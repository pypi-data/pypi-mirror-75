import logging
import math
import os
from typing import TYPE_CHECKING, Callable, Dict, Iterable, List, Optional, Union

import torch
from fastprogress import master_bar, progress_bar
from overrides import overrides
from torch.optim.lr_scheduler import _LRScheduler

from ..common.utils import lazy_groups_of
from ..training import util as training_util
from .trainer import Trainer

if TYPE_CHECKING:
    from ..data.instance import Instance  # noqa: F401
    from ..data.iterators.data_iterator import DataIterator
    from ..models.model import Model

logger = logging.getLogger(__name__)

try:
    from apex import amp
except ImportError:
    logger.info("Apex is not found. So you can't use fp16 training.")


class DistillationTrainer(Trainer):
    def __init__(
        self,
        student_model: "Model",
        teacher_model: "Model",
        optimizer: torch.optim.Optimizer,  # type: ignore
        serialization_dir: str,
        iterator: "DataIterator",
        train_dataset: Iterable["Instance"],
        validation_dataset: Optional[Iterable["Instance"]] = None,
        early_stopping: bool = False,
        patience: Optional[int] = None,
        early_stopping_metric: str = "-loss",
        validation_iterator: Optional["DataIterator"] = None,
        shuffle: bool = True,
        num_epochs: int = 20,
        accumulation_steps: int = 0,
        comparision_loss: torch.nn.modules.loss._Loss = torch.nn.MSELoss(),
        logits_postprocessing: Optional[Callable[[torch.Tensor], torch.Tensor]] = None,
        comparision_loss_weight: float = 0.5,
        experiment_name: Optional[str] = None,
        cuda_device: Union[int, List[int]] = -1,
        grad_norm: Optional[float] = 1.0,
        get_lr_scheduler: Optional[Callable[[torch.optim.Optimizer, float, int], _LRScheduler]] = None,  # type: ignore
        scheduler_warm_up: float = 0.1,
        tf_logging: bool = True,
        tb_logging_dir: str = "tb_logs",
        fp16: bool = False,
        fp16_opt_level: str = "O1",
        gradual_unfreezing_steps: Optional[List[List[str]]] = None,
        checkpoint_steps: Optional[int] = None,
    ) -> None:

        super().__init__(
            model=student_model,
            optimizer=optimizer,
            serialization_dir=serialization_dir,
            iterator=iterator,
            train_dataset=train_dataset,
            validation_dataset=validation_dataset,
            early_stopping=early_stopping,
            patience=patience,
            early_stopping_metric=early_stopping_metric,
            validation_iterator=validation_iterator,
            shuffle=shuffle,
            num_epochs=num_epochs,
            accumulation_steps=accumulation_steps,
            experiment_name=experiment_name,
            cuda_device=cuda_device,
            grad_norm=grad_norm,
            get_lr_scheduler=get_lr_scheduler,
            scheduler_warm_up=scheduler_warm_up,
            tf_logging=tf_logging,
            tb_logging_dir=tb_logging_dir,
            fp16=fp16,
            fp16_opt_level=fp16_opt_level,
            gradual_unfreezing_steps=gradual_unfreezing_steps,
            checkpoint_steps=checkpoint_steps,
        )

        self._teacher_model = teacher_model
        self._comparision_loss_weight = comparision_loss_weight
        self._comparision_loss = comparision_loss
        self._logits_postprocessing = logits_postprocessing

    @overrides  # type: ignore
    def _train_epoch(self, master_bar_logger: master_bar, epoch: int) -> Dict[str, float]:
        """
        Trains one epoch and returns metrics.
        """

        train_loss = 0.0
        # Set the model to "train" mode.
        self._model.train()
        self._model.zero_grad()
        self._teacher_model.eval()
        num_gpus = len(self._cuda_devices)

        raw_train_generator = self._iterator(self._train_data, num_epochs=1, shuffle=self._shuffle)
        train_generator = lazy_groups_of(raw_train_generator, num_gpus)
        num_training_batches = math.ceil(self._iterator.get_num_batches(self._train_data) / num_gpus)

        batches_this_epoch = 0
        global_steps = 0
        for batch_group in progress_bar(
            train_generator, total=num_training_batches, parent=master_bar_logger, leave=False
        ):
            batches_this_epoch += 1

            logits_student, loss = self._batch_outputs_and_loss(self._model, batch_group)

            with torch.no_grad():
                logits_teacher, _ = self._batch_outputs_and_loss(self._teacher_model, batch_group)

            if self._logits_postprocessing is not None:
                logits_student = self._logits_postprocessing(logits_student)
                logits_teacher = self._logits_postprocessing(logits_teacher)

            loss_comparision = self._comparision_loss(logits_student, logits_teacher)
            if self._accumulation_steps > 1:
                loss = loss / self._accumulation_steps
                loss_comparision = loss_comparision / self._accumulation_steps

            loss = self._comparision_loss_weight * loss_comparision + (1 - self._comparision_loss_weight) * loss

            if torch.isnan(loss):
                raise ValueError("nan loss encountered")

            if self._fp16:
                with amp.scale_loss(loss, self._optimizer) as scaled_loss:
                    scaled_loss.backward()
                torch.nn.utils.clip_grad_norm_(amp.master_params(self._optimizer), self._grad_norm)  # type: ignore
            else:
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self._model.parameters(), self._grad_norm)  # type: ignore

            train_loss += loss.item()
            if batches_this_epoch % self._accumulation_steps == 0:
                self._optimizer.step()
                if self._lr_scheduler is not None:
                    self._lr_scheduler.step()  # type: ignore
                self._model.zero_grad()
                global_steps += 1

                master_bar_logger.child.comment = f"loss: {round(train_loss / global_steps, 4)}"

            if self._checkpoint_steps is not None and batches_this_epoch % self._checkpoint_steps == 0:
                checkpoint_folder = os.path.join(
                    self._serialization_dir, f"epoch_{epoch}_checkpoint_{batches_this_epoch}"
                )
                if not os.path.exists(checkpoint_folder):
                    os.makedirs(checkpoint_folder)

                self._model.save(checkpoint_folder)
                with open(os.path.join(checkpoint_folder, "model.th"), "wb") as f:
                    torch.save(self._model.state_dict(), f)  # type: ignore

        metrics = training_util.get_metrics(self._model, train_loss, global_steps, reset=True)
        return metrics  # type: ignore

    @overrides  # type: ignore
    def _validation_run(self, master_bar_logger: master_bar) -> Optional[Dict[str, float]]:
        """
        Computes the validation metrics. Returns it and the number of batches.
        """
        if self._validation_data is None:
            return None

        logger.info("Validating")

        self._model.eval()
        self._teacher_model.eval()

        if self._validation_iterator is not None:
            val_iterator = self._validation_iterator
        else:
            val_iterator = self._iterator

        num_gpus = len(self._cuda_devices)

        raw_val_generator = val_iterator(self._validation_data, num_epochs=1, shuffle=False)
        val_generator = lazy_groups_of(raw_val_generator, num_gpus)
        num_training_batches = math.ceil(self._iterator.get_num_batches(self._validation_data) / num_gpus)

        batches_this_epoch = 0
        val_loss = 0
        for batch_group in progress_bar(
            val_generator, total=num_training_batches, parent=master_bar_logger, leave=False
        ):
            logits_student, loss = self._batch_outputs_and_loss(self._model, batch_group)
            logits_teacher, _ = self._batch_outputs_and_loss(self._teacher_model, batch_group)

            loss_comparision = self._comparision_loss(logits_student, logits_teacher)
            loss = self._comparision_loss_weight * loss_comparision + (1 - self._comparision_loss_weight) * loss

            batches_this_epoch += 1
            val_loss += loss.detach().cpu().numpy()
        val_metrics = training_util.get_metrics(self._model, val_loss, batches_this_epoch, reset=True)
        return val_metrics  # type: ignore

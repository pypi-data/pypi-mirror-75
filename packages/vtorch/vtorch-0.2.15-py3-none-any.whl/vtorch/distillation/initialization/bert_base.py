import os
from typing import Dict

from transformers import BertConfig, BertModel

from vtorch.data import Vocabulary

from ...common.checks import ConfigurationError
from ...models import Model
from ...models.model_parameters import ModelParameters


class BertBaseInitializer:
    def __init__(self, teacher_model: Model, student_model: Model) -> None:
        self.teacher_model = teacher_model
        self.student_model = student_model

    def _transfer_weights(self) -> None:
        teacher_model_weights = self.teacher_model.state_dict()
        student_model_weights = self.student_model.state_dict()

        for name, weights in student_model_weights.items():
            if (
                name.startswith("_transformer.embeddings")
                or name.startswith("_transformer.pooler")
                or name.startswith("_classification_head")
            ):
                student_model_weights[name] = teacher_model_weights[name]

        for name, weights in student_model_weights.items():
            for teacher_index in [0, 2, 4, 7, 9, 11]:
                student_index = int(teacher_index / 2)
                if name.startswith(f"_transformer.encoder.layer.{student_index}"):
                    student_model_weights[name] = teacher_model_weights[
                        name.replace(str(student_index), str(teacher_index))
                    ]

        self.student_model.load_state_dict(student_model_weights)

    def save_student_model_initialized_with_teacher_weights(self, path: str) -> None:
        self._transfer_weights()
        self.student_model.save(path)

    @classmethod
    def load(cls, teacher_model_path: str, models_mapping: Dict[str, Model]) -> "BertBaseInitializer":
        teacher_model_parameters, teacher_model_type_name = ModelParameters.load(teacher_model_path)
        if teacher_model_type_name is None:
            raise ValueError("There is no model type in model parameters file. Check model parameters.")
        teacher_model_type = models_mapping[teacher_model_type_name]
        teacher_model = teacher_model_type.load(
            model_params=teacher_model_parameters, serialization_dir=teacher_model_path
        )

        student_model_transformer_config = BertConfig.from_pretrained(teacher_model_path)
        if student_model_transformer_config.num_hidden_layers != 12:
            raise ConfigurationError("You can load only bert-base configuration with 12 transformer layers")
        student_model_transformer_config.num_hidden_layers = 6
        bert_transformer = BertModel(student_model_transformer_config)

        teacher_model_vocabulary = Vocabulary.from_files(os.path.join(teacher_model_path, "vocabulary"))

        student_model = teacher_model_type(
            bert_transformer, vocab=teacher_model_vocabulary, model_params=teacher_model_parameters
        )

        return cls(teacher_model, student_model)

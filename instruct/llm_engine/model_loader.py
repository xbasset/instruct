import logging
import os
from typing import List
import yaml
from instruct.llm_engine.model import Model


logging.basicConfig(level=logging.ERROR)

class ModelLoader:
    models_conf_filename = "~/.instruct/models.yaml"
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.models: list[Model] = self._load_models()
            self._initialized = True

    def _load_models(self):
        try:
            with open(os.path.expanduser(self.models_conf_filename), "r") as f:
                config = yaml.load(f, Loader=yaml.FullLoader) or {}

            model_list: List[Model] = []
            for _, models_data in config.items():
                for conf_model, data in models_data.items():
                    model = conf_model
                    provider = Model(model=model, **data)
                    model_list.append(provider)
            return model_list

        except Exception as e:
            logging.error(f"Error loading {self.models_conf_filename}: {e}")
            return []


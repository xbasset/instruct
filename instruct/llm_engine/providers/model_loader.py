import configparser
import logging
import os
import yaml
from rich.console import Console
from instruct.llm_engine.model import Model

from instruct.llm_engine.providers import provider_map

logging.basicConfig(level=logging.ERROR)
console = Console()


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
            self.providers: list[Model] = self._load_providers()
            self._initialized = True

    def _load_providers(self):
        try:
            with open(os.path.expanduser(self.models_conf_filename), "r") as f:
                config = yaml.load(f, Loader=yaml.FullLoader) or {}

            providers = []
            for provider_name, provider_data in config.items():
                for model_type, models in provider_data.items():
                    for model_name, model_config in models.items():
                        provider = self._build_provider(
                            provider_name, model_name, model_type, model_config
                        )
                        if provider is not None:
                            providers.append(provider)

            return providers
        except Exception as e:
            logging.error(f"Error loading {self.models_conf_filename}: {e}")
            return []

    def _build_provider(self, provider_name, model_name, model_type, conf):
        try:
            # Handle nested provider map for Azure
            if provider_name == "azure":
                client_name = conf.get("client")
            else:
                client_name = provider_name

            model_class = provider_map.get(client_name, {}).get(model_type, {})

            if model_class:
                model_instance = model_class({"model": model_name, **conf})
                model_instance.provider = provider_name
                model_instance.type = model_type
                model_instance.name = model_name
                return model_instance
            else:
                logging.warning(
                    f"Provider {provider_name} with model type {model_type} and model {model_name} not recognized."
                )
        except Exception as e:
            logging.error(
                f"Error initializing {provider_name} with model type {model_type} for model {model_name}: {e}"
            )
        return None

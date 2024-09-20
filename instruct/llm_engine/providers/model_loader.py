import configparser
import logging
import os
import yaml
from rich.console import Console

from instruct.llm_engine.providers import OpenAILLM, MistralAILLM, OllamaLLM, OpenAIVisionLLM, GroqLLM, provider_map

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
            self.providers = self._load_providers()
            self._initialized = True

    def _load_providers(self):
        try:
            with open(os.path.expanduser(self.models_conf_filename), 'r') as f:
                config = yaml.load(f, Loader=yaml.FullLoader) or {}
            return [
                provider
                for p_name, models in config.items()
                for m_name in models
                if (provider := self._build_provider(p_name, m_name, config[p_name])) is not None
            ]
        except Exception as e:
            logging.error(f"Error loading {self.models_conf_filename}: {e}")
            return []

    def _build_provider(self, provider_name, model, conf):
        try:
            # logging.info(f"Building provider {provider_name} for model {model}")
            model_class = provider_map.get(provider_name)
            if model_class:
                return model_class({"model": model, **conf})
            if provider_name == "azure" and model == "gpt4-vision":
                return OpenAIVisionLLM(conf)
            logging.warning(f"Unimplemented provider: {provider_name}")
        except Exception as e:
            logging.error(f"Error building provider {provider_name}: {e}")
        return None

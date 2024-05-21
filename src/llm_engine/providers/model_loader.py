import configparser

from src.llm_engine.model import Model
from src.llm_engine.providers.openai_llm import OpenAILLM
from src.llm_engine.providers.mistralai_llm import MistralAILLM
from src.llm_engine.providers.ollama_llm import OllamaLLM
from src.llm_engine.providers.openai_vision_llm import OpenAIVisionLLM
from src.llm_engine.providers.groq_llm import GroqLLM

import logging
import os
import yaml

logging.basicConfig(level=logging.ERROR)


class ModelLoader:
    llm_conf_filename = "models.yaml"
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ModelLoader, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.providers = self._get_providers()

    def _get_providers(self):
        """
        Returns the list of available LLM providers in the models.yaml file

        """
        try:
            llm_providers_list = []
            
            with open(ModelLoader.llm_conf_filename, 'r') as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
            
            providers = config

            for provider_name, conf in providers.items():
                for model_name in conf:
                    llm = self._build_provider(
                        provider_name, model_name, conf)
                    provider_conf = {
                        "model_name": model_name,
                        "provider_name": provider_name,
                        "provider": llm,
                        "config": conf
                    }
                    llm_providers_list.append(provider_conf)

            return llm_providers_list

        except Exception as e:
            logging.error(
                f"🔴: ERROR: {ModelLoader.__subclasses__()[0].__name__} >> {e}")
            return []

    def _build_provider(self, provider_name, model_name, conf):
        """
        Build a provider object from the provider name and model name.
        """
        try:
            model = None
            provider_conf = conf[model_name]

            
            if provider_name == "openai":
                conf = {
                    "api_key": provider_conf["openai_api_key"],
                    "api_type": provider_name,
                    "model_name": model_name
                }
                model = OpenAILLM(conf)

            elif provider_name == "azure":
                conf = {
                    "api_key": provider_conf["api_key"],
                    "api_base": provider_conf["endpoint"], # for OpenAI models
                    "endpoint": provider_conf["endpoint"], # for Mistral models
                    "api_type": provider_name,
                    "api_version": provider_conf["api_version"],
                    "deployment_id": provider_conf["deployment_id"],
                    "model_name": model_name
                }
                if model_name in ["gpt4-turbo", "gpt-4-turbo", "gpt4-32k", "gpt-4o"]:
                    model = OpenAILLM(conf)
                elif model_name == "gpt4-vision":
                    model = OpenAIVisionLLM(conf)
                elif model_name == "mistral-large":
                    model = MistralAILLM(conf)

            elif provider_name == "mistral":
                conf = {
                    "api_key": provider_conf["api_key"],
                    "api_model": model_name,
                    "model_name": model_name
                }
                model = MistralAILLM(conf)

            elif provider_name == "ollama":
                conf = {
                    "endpoint": provider_conf["ollama_endpoint"],
                    "model": model_name,
                    "model_name": model_name
                }
                model = OllamaLLM(conf)
            
            elif provider_name == "groq":
                conf = {
                    "api_key": provider_conf["api_key"],
                    "model": model_name,
                    "model_name": model_name
                }
                model = GroqLLM(conf)

            if provider_name not in ["openai", "azure", "mistral", "ollama", "groq"]:
                logging.warning(
                    f"🔴: ERROR: ModelLoader _build_provider() >> in config file {ModelLoader.llm_conf_filename} provider: ** {provider_name} ** has not been implemented")

            return model
        except Exception as e:
            logging.error(f"🔴: ERROR: ModelLoader _build_provider() >> {e}")
            return None



    def _get_providers_by_model(self, model):
        """
        Return a list of providers that support the given model.
        The providers are encoded in the sections of the config file as the following format <provider>/<model>
        """
        conf_file = os.path.join(os.path.dirname(
            __file__), ModelLoader.llm_conf_filename)
        config = configparser.ConfigParser()
        config.read(conf_file)
        providers = []
        for section in config.sections():
            provider, model_name = section.split('/')
            if model_name == model:
                providers.append(provider)
        return providers

    def _get_all_models(self):
        """
        Return a list of all models in the config file.
        """
        conf_file = os.path.join(os.path.dirname(
            __file__), ModelLoader.llm_conf_filename)
        config = configparser.ConfigParser()
        config.read(conf_file)
        models = []
        for section in config.sections():
            provider, model_name = section.split('/')
            models.append(model_name)
        return set(models)

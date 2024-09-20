from .openai_llm import OpenAILLM
from .mistralai_llm import MistralAILLM
from .ollama_llm import OllamaLLM
from .openai_vision_llm import OpenAIVisionModel
from .groq_llm import GroqLLM

provider_map = {
    "openai": {"llm": OpenAILLM, "vision": OpenAIVisionModel},
    "mistral": {"llm": MistralAILLM},
    "ollama": {
        "llm": OllamaLLM,
    },
    "groq": {
        "llm": GroqLLM,
    },
}

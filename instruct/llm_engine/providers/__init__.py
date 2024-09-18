from .openai_llm import OpenAILLM
from .mistralai_llm import MistralAILLM
from .ollama_llm import OllamaLLM
from .openai_vision_llm import OpenAIVisionLLM
from .groq_llm import GroqLLM

provider_map = {
    "openai": OpenAILLM,
    "mistral": MistralAILLM,
    "ollama": OllamaLLM,
    "groq": GroqLLM,
}
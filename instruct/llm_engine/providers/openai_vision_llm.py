from openai import OpenAI, AzureOpenAI, RateLimitError
from instruct.llm_engine.model import Model
from instruct.llm_engine.providers.openai_llm import OpenAILLM
import tiktoken
import logging
from typing import List

from instruct.instruct import Instruct


class OpenAIVisionLLM(OpenAILLM):

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    def __init__(self, llm_conf):
        super().__init__(llm_conf)

    @staticmethod
    def get_image_message_url_prefix(image_name):
        try:
            extension = image_name.split(".")[-1].lower()
            # check if extension is allowed
            if extension not in OpenAIVisionLLM.ALLOWED_EXTENSIONS:
                raise Exception(f"Image extension not allowed: {extension}")
            return 'data:image/' + extension
        except Exception as e:
            raise Exception(f"_get_image_message_url_prefix :: {e}")

    def recursive_invoke(self, messages, user_id, temperature, max_tokens, frequency_penalty, presence_penalty,
                         stream=False, stream_callback=None, user_task_execution_pk=None, task_name_for_system=None,
                         n_additional_calls_if_finish_reason_is_length=0, **kwargs):
        try:

            responses = self._call_completion_with_rate_limit_management(messages, self.user_id, temperature, max_tokens,
                                                                         frequency_penalty, presence_penalty,
                                                                         stream, stream_callback,
                                                                         n_additional_calls_if_finish_reason_is_length,
                                                                         **kwargs)

            return responses
        except Exception as e:
            raise Exception(
                f"🔴 Error in OpenAI recursive_invoke() > - model: {self.name}")

from openai import OpenAI, AzureOpenAI, RateLimitError
from instruct.llm_engine.model import Model
import tiktoken
import uuid

import logging
from typing import List


import os

from instruct.instruct import Instruct


class OpenAILLM(Model):

    def __init__(self, llm_conf):
        """
        :param api_key: API key to call openAI
        :param api_base: Endpoint to call openAI
        :param api_version: Version of the API to user
        :param model: Model to use (deployment_id for azure)
        :param api_type: 'azure' or 'openai'
        """
        try:
            self._name = llm_conf["model_name"]
            api_key = llm_conf["api_key"]
            api_base = llm_conf["api_base"] if "api_base" in llm_conf else None
            api_version = llm_conf["api_version"] if "api_version" in llm_conf else None
            api_type = llm_conf["api_type"] if "api_type" in llm_conf else "openai"
            self.deployment = llm_conf["deployment_id"] if "deployment_id" in llm_conf else None

            # user_id for openAI moderation
            self.user_id = uuid.uuid4()

            self.client = AzureOpenAI(
                api_version=api_version,
                azure_endpoint=api_base,
                azure_deployment=self.deployment,
                api_key=api_key
            ) if api_type == 'azure' else OpenAI(api_key=api_key)

            self.client_backup = None

            Model.__init__(
                self, llm_conf)
        except Exception as e:
            raise Exception(f"🔴 Error initializing OpenAILLM __init__  : {e}")

    def _handle_chat_completion_response(self, completion, stream, stream_callback):
        try:
            if stream:
                complete_text = ""
                finish_reason = None
                for stream_chunk in completion:
                    choice = stream_chunk.choices[0]
                    partial_token = choice.delta
                    finish_reason = choice.finish_reason
                    if partial_token.content:
                        complete_text += partial_token.content
                        if stream_callback is not None:
                            try:
                                flag_to_stop_streaming = stream_callback(
                                    complete_text)
                                if flag_to_stop_streaming:
                                    return None
                            except Exception as e:
                                logging.error(
                                    f"🔴 Error in streamCallback: {e}")

                response = complete_text
            else:
                response = completion.choices[0].message.content
                finish_reason = completion.choices[0].finish_reason

            return response, finish_reason
        except Exception as e:
            raise Exception(f"_handle_chat_completion_stream : {e}")

    def chatCompletion(self, messages, user_uuid, temperature, max_tokens, frequency_penalty=0, presence_penalty=0, stream=False, stream_callback=None,
                       n_additional_calls_if_finish_reason_is_length=0, assistant_response="", n_calls=0, use_backup_client=False, **kwargs):
        """
        OpenAI chat completion
        :param messages: List of messages composing the conversation, each message is a dict with keys "role" and "content"
        :param user_uuid: Compulsory for openAI to track harmful content. If a user tries to pass the openAI moderation, we will receive an email with this id and we can go back to him to remove his access.
        :param temperature: The higher the temperature, the crazier the text
        :param max_tokens: The maximum number of tokens to generate
        :param frequency_penalty: The higher the penalty, the less likely the model is to repeat itself
        :param presence_penalty: The higher the penalty, the less likely the model is to generate a response that is similar to the prompt
        :param stream: If True, will stream the completion
        :param stream_callback: If stream is True, will call this function with the completion as parameter
        :param n_additional_calls_if_finish_reason_is_length: If the finish reason is "length", will relaunch the function, instructing the assistant to continue its response
        :param assistant_response: Assistant response to add to the completion
        :param n_calls: Number of calls to the function
        :return: List of n generated messages
        """
        openai_client = self.client_backup if use_backup_client else self.client

        # if "json_format" in kwargs and kwargs["json_format"]:
        # set response_format={"type": "json_object"} in kwargs
        if "json_format" in kwargs and kwargs["json_format"]:
            kwargs.pop("json_format")
            kwargs["response_format"] = {"type": "json_object"}

        completion = openai_client.chat.completions.create(
            messages=messages,
            model=self.name,
            temperature=temperature,
            max_tokens=max_tokens,
            user=user_uuid,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stream=stream,
            **kwargs
        )

        response, finish_reason = self._handle_chat_completion_response(
            completion, stream, stream_callback)

        if finish_reason == "length" and n_calls < n_additional_calls_if_finish_reason_is_length:
            # recall the function with assistant_message + user_message
            messages = messages + [{'role': 'assistant', 'content': response},
                                   {'role': 'user', 'content': 'Continue'}]
            return self.chatCompletion(messages, user_uuid, temperature, max_tokens,
                                       frequency_penalty=frequency_penalty, presence_penalty=presence_penalty,
                                       stream=stream, stream_callback=stream_callback,
                                       assistant_response=assistant_response + " " + response,
                                       n_additional_calls_if_finish_reason_is_length=n_additional_calls_if_finish_reason_is_length,
                                       n_calls=n_calls + 1, **kwargs)
        # [] is a legacy from the previous version that could return several completions. Need complete refacto to remove.
        return [assistant_response + " " + response]

    def invoke_from_pt(self, instruct: Instruct, temperature, max_tokens, frequency_penalty=0, presence_penalty=0,
                        stream=False, stream_callback=None, **kwargs):
        try:


            if self.name not in instruct.models:
                logging.warning(
                    f"{pt} does not contain model: {self.name} in its dashbangs")
            messages = [{"role": "user", "content": instruct.prompt}]
            responses = self.recursive_invoke(messages, temperature, max_tokens,
                                              frequency_penalty=frequency_penalty, presence_penalty=presence_penalty,
                                              stream=stream, stream_callback=stream_callback,
                                              n_additional_calls_if_finish_reason_is_length=0, **kwargs)
            return responses
        except Exception as e:
            raise Exception(
                f"🔴 Error in OpenAILLM invoke: {e} - model: {self.name}"
            )

    def invoke(self, messages: List, temperature, max_tokens,
               frequency_penalty=0, presence_penalty=0, stream=False, stream_callback=None, **kwargs):
        return self.recursive_invoke(messages, temperature, max_tokens,
                                     frequency_penalty=frequency_penalty, presence_penalty=presence_penalty,
                                     stream=stream, stream_callback=stream_callback,
                                     n_additional_calls_if_finish_reason_is_length=0, **kwargs)

    def _call_completion_with_rate_limit_management(self, messages, temperature, max_tokens, frequency_penalty, presence_penalty,
                                                    stream, stream_callback,
                                                    n_additional_calls_if_finish_reason_is_length, **kwargs):
        try:
            try:
                return self.chatCompletion(messages, str(self.user_id), temperature, max_tokens, frequency_penalty, presence_penalty, stream=stream,
                                           stream_callback=stream_callback,
                                           n_additional_calls_if_finish_reason_is_length=n_additional_calls_if_finish_reason_is_length,
                                           **kwargs)
            except RateLimitError:
                # try to use backup engine
                if self.client_backup:
                    return self.chatCompletion(messages, str(self.user_id), temperature, max_tokens, frequency_penalty, presence_penalty,
                                               stream=stream,
                                               stream_callback=stream_callback,
                                               use_backup_client=True, **kwargs)
                else:
                    raise Exception(
                        "Rate limit exceeded and no backup engine available")
        except Exception as e:
            raise Exception(
                f"_call_completion_with_rate_limit_management : {e}")

    def recursive_invoke(self, messages, temperature, max_tokens, frequency_penalty=0, presence_penalty=0,
                         stream=False, stream_callback=None,
                         n_additional_calls_if_finish_reason_is_length=0, **kwargs):
        try:

            responses = self._call_completion_with_rate_limit_management(messages, temperature, max_tokens,
                                                                         frequency_penalty, presence_penalty,
                                                                         stream, stream_callback,
                                                                         n_additional_calls_if_finish_reason_is_length,
                                                                         **kwargs)
            return responses
        except Exception as e:
            raise Exception(
                f"🔴 Error in OpenAILLM recursive_invoke() > {e} - model: {self.name}")



import os
from instruct.llm_engine.model import Model
from instruct.instruct import Instruct

import logging


from ollama import Client


class OllamaLLM(Model):

    def __init__(self, ollama_conf):

        try:
            self._name = ollama_conf["model"]
            self.model = ollama_conf.get(
                "model") if ollama_conf.get("model") else None
            self.endpoint = ollama_conf.get("endpoint") if ollama_conf.get(
                "endpoint") else None

            if self.endpoint is None or self.model is None:
                raise Exception(
                    f"🔴 model and endpoint not set in models conf: {ollama_conf}")

            self.client = Client(host=self.endpoint)

        except Exception as e:
            raise Exception(
                f"🔴 Error initializing OllamaLLM __init__  : {e}")

    def chatCompletion(self, messages, temperature, max_tokens, n_responses=1,
                       frequency_penalty=0, presence_penalty=0, stream=False, stream_callback=None, json_format=False):
        try:
            # ensure if stream is true, n_responses = 1
            if stream and n_responses != 1:
                n_responses = 1
                logging.warning("n_responses must be 1 if stream is True")

            if stream:

                stream_response = self.client.chat(
                    model=self.model,
                    messages=messages,
                    stream=True,
                )

                complete_text = ""
                for chunk in stream_response:
                    partial_token = chunk['message']['content']
                    complete_text += partial_token if partial_token else ""
                    if stream_callback is not None:
                        try:
                            stream_callback(complete_text)
                        except Exception as e:
                            logging.error(
                                f"🔴 Error in streamCallback : {e}")
            else:
                response = self.client.chat(
                    model=self.model, messages=messages)

                complete_text = response['message']['content']
            # [content.text for content in stream_response.choices]
            return [complete_text]

        except Exception as e:
            logging.error(f"Error in OllamaLLM chat: {e}")

    def invoke(self, messages, temperature, max_tokens, n_responses=1,
               frequency_penalty=0, presence_penalty=0, stream=False, stream_callback=None, json_format=False):
        try:

            responses = self.chatCompletion(messages, temperature, max_tokens, n_responses=n_responses,
                                            frequency_penalty=frequency_penalty, presence_penalty=presence_penalty, stream=stream, stream_callback=stream_callback, json_format=json_format)

            return responses
        except Exception as e:
            raise Exception(
                f"🔴 Error in OllamaAILLM: {e} - model: {self.model}")

    def invoke_from_pt(self, instruct: Instruct, temperature, max_tokens, n_responses=1,
                        frequency_penalty=0, presence_penalty=0, stream=False, stream_callback=None, json_format=False):
        try:

            if self.model not in instruct.models:
                logging.warning(
                    f"{pt} does not contain model: {self.model} in its dashbangs")

            messages = [{"role": "user", "content": instruct.prompt}]
            responses = self.invoke(messages, temperature, max_tokens, n_responses=n_responses,
                                    frequency_penalty=frequency_penalty, presence_penalty=presence_penalty, stream=stream, stream_callback=stream_callback, json_format=json_format)
            return responses
        except Exception as e:
            raise Exception(
                f"🔴 Error in OllamaAILLM: > {e} - model: {self.model}")

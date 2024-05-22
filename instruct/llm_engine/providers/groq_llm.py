

import os
from instruct.llm_engine.model import Model
from instruct.pt import PT

import logging

from groq import Groq

class GroqLLM(Model):

    def __init__(self, groq_conf):

        try:
            self._name = groq_conf["model_name"]
            self.model = groq_conf.get(
                "model") if groq_conf.get("model") else None

            if self.model is None:
                raise Exception(
                    f"🔴 model not set in models conf: {groq_conf}")

            self.client = Groq(api_key=groq_conf["api_key"])

        except Exception as e:
            raise Exception(
                f"🔴 Error initializing GroqLLM __init__  : {e}")

    def chatCompletion(self, messages, temperature, max_tokens, n_responses=1,
                       frequency_penalty=0, presence_penalty=0, stream=False, stream_callback=None, json_format=False):
        try:
            # ensure if stream is true, n_responses = 1
            if stream and n_responses != 1:
                n_responses = 1
                logging.warning("n_responses must be 1 if stream is True")

            if stream:
                stream_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    stream=True,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                complete_text = ""
                for chunk in stream_response:
                    partial_token = chunk.choices[0].delta.content
                    complete_text += partial_token if partial_token else ""
                    if stream_callback is not None:
                        try:
                            stream_callback(complete_text)
                        except Exception as e:
                            logging.error(
                                f"🔴 Error in streamCallback : {e}")
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                    )

                complete_text = response.choices[0].message.content
            # [content.text for content in stream_response.choices]
            return [complete_text]

        except Exception as e:
            logging.error(f"Error in GroqLLM chat: {e}")

    def invoke(self, messages, temperature, max_tokens, n_responses=1,
               frequency_penalty=0, presence_penalty=0, stream=False, stream_callback=None, json_format=False):
        try:

            responses = self.chatCompletion(messages, temperature, max_tokens, n_responses=n_responses,
                                            frequency_penalty=frequency_penalty, presence_penalty=presence_penalty, stream=stream, stream_callback=stream_callback, json_format=json_format)

            return responses
        except Exception as e:
            raise Exception(
                f"🔴 Error in GroqLLM: {e} - model: {self.model}")

    def invoke_from_pt(self, pt: PT, temperature, max_tokens, n_responses=1,
                        frequency_penalty=0, presence_penalty=0, stream=False, stream_callback=None, json_format=False):
        try:

            if self.model not in pt.models:
                logging.warning(
                    f"{pt} does not contain model: {self.model} in its dashbangs")

            messages = [{"role": "user", "content": pt.prompt}]
            responses = self.invoke(messages, temperature, max_tokens, n_responses=n_responses,
                                    frequency_penalty=frequency_penalty, presence_penalty=presence_penalty, stream=stream, stream_callback=stream_callback, json_format=json_format)
            return responses
        except Exception as e:
            raise Exception(
                f"🔴 Error in GroqLLM: > {e} - model: {self.model}")

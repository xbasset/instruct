from mistralai import Mistral
import logging
import os
from instruct.llm_engine.model import Model
from instruct.instruct import Instruct

logging.basicConfig(level=logging.ERROR)


class MistralAILLM(Model):

    def __init__(self, model_conf):

        try:

            self._name = model_conf["model"]
            api_key = model_conf["api_key"]
            self.model = self._name
            

            endpoint = model_conf.get("endpoint") if model_conf.get(
                "endpoint") else None
            api_type = "azure" if model_conf.get(
                "endpoint") else "la_plateforme"

            self.client = Mistral(
                api_key=api_key,
                server_url=endpoint if api_type == 'azure' else "https://api.mistral.ai",
            )

        except Exception as e:
            raise Exception(
                f"🔴 Error initializing MistralAILLM __init__  : {e}")

    def chatCompletion(self, messages, temperature, max_tokens, n_responses=1,
                       frequency_penalty=0, presence_penalty=0, stream=False, stream_callback=None, json_format=False):
        try:
            # ensure if stream is true, n_responses = 1
            if stream and n_responses != 1:
                n_responses = 1
                logging.warning("n_responses must be 1 if stream is True")

            if len(messages) == 1:
                messages = [
                    {"role":'user', "content":messages[0]['content']}]
            else:
                messages = [{"role":message['role'], "content":message['content']} for message in messages]

            if stream:
                stream_response = self.client.chat.stream(
                    model=self.model, messages=messages, temperature=temperature, max_tokens=max_tokens)

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
                response = self.client.chat.complete(
                    model=self.model, messages=messages, temperature=temperature, max_tokens=max_tokens)

                complete_text = response.choices[0].message.content
            # [content.text for content in stream_response.choices]
            return [complete_text]

        except Exception as e:
            logging.error(f"💨❌: Error in MistralAILLM: {e}")

    def invoke(self, messages, temperature, max_tokens, n_responses=1,
               frequency_penalty=0, presence_penalty=0, stream=False, stream_callback=None, json_format=False):
        try:

            responses = self.chatCompletion(messages, temperature, max_tokens, n_responses=n_responses,
                                            frequency_penalty=frequency_penalty, presence_penalty=presence_penalty, stream=stream, stream_callback=stream_callback, json_format=json_format)

            return responses
        except Exception as e:
            raise Exception(
                f"🔴 Error in MistralAILLM.invoke: {e} - model: {self.model}")

    def invoke_from_pt(self, instruct: Instruct, temperature, max_tokens, n_responses=1,
                        frequency_penalty=0, presence_penalty=0, stream=False, stream_callback=None, json_format=False):
        try:

            if self.model not in instruct.models:
                logging.warning(
                    f"{instruct} does not contain model: {self.model} in its dashbangs")
            messages = [{"role": "user", "content": instruct.prompt}]
            responses = self.invoke(messages, temperature, max_tokens, n_responses=n_responses,
                                    frequency_penalty=frequency_penalty, presence_penalty=presence_penalty, stream=stream, stream_callback=stream_callback, json_format=json_format)
            return responses
        except Exception as e:
            raise Exception(
                f"Error in Mistral AI chat : {e}")



if __name__ == "__main__":

    api_key = "GImprxgjZDsnnsH1eTpOK8nqWySbM2tV"
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
                "role": "user",
                "content": "What is the best French cheese?",
            },
        ]
    )
    print(chat_response.choices[0].message.content)
import logging
from litellm import completion

logging.basicConfig(level=logging.ERROR)


class Model:
    """
    Abstract base class for Model implementations.
    """

    def __init__(
        self,
        model: str,
        name: str,
        api_key: str = None,
        api_version: str = None,
        base_url: str = None,
        **kwargs,
    ):
        """
        Initializes the model object.

        Args:
            model_conf (dict): The configuration for the model.
        """
        self.model = model
        self.name = name
        self.api_key = api_key
        self.api_version = api_version
        self.base_url = base_url


    def invoke(
        self, messages, temperature, max_tokens, stream=False, stream_callback=None
    ):
        """
        Perform a Model chat completion.

        Args:
            messages (list): List of messages.
            temperature (float): Temperature parameter for generating responses.
            max_tokens (int): Maximum number of tokens in the generated response.
            stream (bool): Whether to stream the response.
            stream_callback (function): Callback function for streaming.

        Returns:
            None
        """
        try:
            completion_result = completion(
                model=self.model,
                api_key=self.api_key,
                api_version=self.api_version,
                base_url=self.base_url,
                messages=messages,
                stream=stream,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            if stream:
                complete_text = ""
                for stream_chunk in completion_result:
                    complete_text += stream_chunk.choices[0].delta.content or ""
                    if stream_callback is not None:
                        try:
                            stream_callback(complete_text)
                        except Exception as e:
                            logging.error(f"🔴 Error in stream_callback: {e}")

                response = complete_text
            else:
                response = completion_result["choices"][0]["message"]["content"]
            return response
        except Exception as e:
            logging.error(f"Error in Model invoke: {e}")

    def interpret(
        self, instruct, temperature, max_tokens, stream=False, stream_callback=None
    ):
        """
        Perform the interpretation of an Instruct object using the Model.

        Args:
            instruct (Instruct): The Instruct object.
            temperature (float): Temperature parameter for generating responses.
            max_tokens (int): Maximum number of tokens in the generated response.
            stream (bool): Whether to stream the response.
            stream_callback (function): Callback function for streaming.

        Returns:
            None
        """
        try:
            messages = [{"role": "user", "content": instruct.prompt}]
            return self.invoke(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
                stream_callback=stream_callback,
            )
        except Exception as e:
            logging.error(f"Error in Model interpret: {e}")

from instruct.instruct import Instruct
import logging

pt = Instruct("examples/instructions/translation.instruct",
        text="Bonjour tout le monde !", language="english")


translation = instruct.run(temperature=0.7, max_tokens=200)

print(translation)

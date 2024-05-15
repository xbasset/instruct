from pt import PT
import logging

pt = PT("examples/instructions/translation.pt",
        text="Bonjour tout le monde !", language="english")


translation = pt.run(temperature=0.7, max_tokens=200)

print(translation)

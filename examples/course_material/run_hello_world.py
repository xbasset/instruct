from instruct.instruct import Instruct

pt = Instruct("examples/course_material/hello_world.instruct", name="Alice")
result = instruct.run(temperature=0.7, max_tokens=50)
print(result)
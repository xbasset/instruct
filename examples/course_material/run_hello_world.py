from instruct.pt import PT

pt = PT("examples/course_material/hello_world.pt", name="Alice")
result = pt.run(temperature=0.7, max_tokens=50)
print(result)
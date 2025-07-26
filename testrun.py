a="""- This is a heading\n- test\n- test2\n- test3"""

b = a.split("\n")


c = list(filter(lambda x: x[:2] == "- ", b))

print(c)




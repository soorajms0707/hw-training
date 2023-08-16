import  ast


# cleaned data

# data = "(1,2,3,4)"""""""""

# a=ast.literal_eval(data)
# print(a)
# print(type(a))


# to parse convert python code to abstract syntax tree 
# data = """
# x = 10
# if x > 5:
#     print("x is greater than 5")
# """
# a=ast.parse(data)
# print(ast.dump(a))

# for node in ast.walk(a):
#     print(type(node).__name__)

# --------------------------- 

# data =  """
# def greet(name):
#     print(f"Hello, {name}!")

# """

# a=ast.parse(data)
# print(ast.dump(a))

# for node in ast.walk(a):
#     if isinstance(node, ast.FunctionDef):
#         print("Found function:", node.name)
#         print(type(node).__name__)
# print(type(node).__name__)






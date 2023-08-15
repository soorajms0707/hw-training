import re
pattern = "[a-zA-Z0-9]+@[a-zA-Z]+\.*(com|edu|net)"
user_input = input()
if(re.search(pattern,user_input)):
    print("valid email")
else:
    print("invalid email")



# -------------------


# pattern = "(\d\d\d)-(\d\d\d)-(/d/d/d/d)"
# new_pattern = r"\1\2\3"
# user_input = input()
# new_user_input = re.sub(pattern,new_pattern, user_input)
# print(new_user_input)

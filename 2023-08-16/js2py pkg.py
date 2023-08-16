import js2py

# j='console.log("hello")'

# a=js2py.eval_js(j)
# print(a)


# context = js2py.EvalJs()


code = '''
function add(a, b) {
    return a + b;
}
'''

b=js2py.eval_js(code)
# context.execute(code)

# Call the JavaScript function from Python
print(b(5,5))  # Output: Result: 8
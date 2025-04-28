def get_examples():
    return [
        {
            "name": "Hello World",
            "code": 'print("Hello, world!")'
        },
        {
            "name": "Basic Loop",
            "code": """
for i in range(10):
    print("Number:", i)
"""
        },
        {
            "name": "Simple Function",
            "code": """
def add_numbers(a, b):
    return a + b

result = add_numbers(3, 5)
print("Result:", result)
"""
        }
    ]

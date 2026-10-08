from functions.run_python_file import run_python_file

print(f'{run_python_file("calculator", "main.py")}')
print(f'{run_python_file("calculator", "main.py", ["3 + 5"])}')
print(f'{run_python_file("calculator", "tests.py")}')
print(f'{run_python_file("calculator", "../main.py")}')
print(f'{run_python_file("calculator", "nonexistent.py")}')
print(f'{run_python_file("calculator", "lorem.txt")}')

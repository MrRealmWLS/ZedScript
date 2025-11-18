import os
import json
import re
import functools
import ZedScript.error as error

useos = False

def get_context(filename: str):
    with open(filename, "r") as file:
        context = file.read().splitlines() 
        return [line.strip() for line in context]


def check_type(value, pc):
    if value.isdigit():
        return "int"
    elif value.replace('.', '', 1).isdigit():
        return "float"
    elif any(op in value for op in ["+", "-", "/", "*"]):
        return "math"
    elif value.startswith("input("):
        return "input"
    elif value.startswith("os.getcwd("):
        return "os.getcwd"
    else:

        value = str(value)
        if value.startswith('"') or value.startswith("'"):
            if value.endswith('"') or value.endswith("'"):
                return "str"
            else:
                error.SyntaxError("'\"' expected at end", line_number=pc)
        elif value == "True" or value == "False":
            return "bool"
        else:
            error.UnknownTypeError(f"The {value} data type is not recognized", line_number=pc)

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def get_string_context(string):
    return string[1:-1]

def Input(line, pc):
    n, text = line.split("input(", 1)
    text = text.replace(")", "", -1)
    text = get_string_context(text)
    r = input(text)
    return f'"{r}"'

def Print(line, pc):
    n, text = line.split("print(", 1)
    text = text.replace(")", "", -1)
    text_type = check_type(text, pc)
    if text_type == "str":
        print(get_string_context(text))
    elif text_type in ["bool", "int", "float"]:
        print(text)
    elif text_type == "math":
        expression = line.replace("Print", "")
        result = math(expression,pc)
        print(result)

def is_empty(string):
    return string.strip() == ""
@functools.lru_cache(maxsize=100)
def get_var_pattern(var_name):
    pattern = rf"\b{re.escape(var_name)}\b"
    return pattern

def concatenate(str1, str2):
    return get_string_context(str1) + get_string_context(str2)

def math(expression,line_number):
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

def make_str(value):
    return f"'{value}'"

def check_dependencies(script_path: str):
    global useos

    base_dir = os.path.dirname(os.path.abspath(script_path))
    deps_path = os.path.join(base_dir, "dependencies.json")

    if not os.path.exists(deps_path):
        error.ImportError(f"Missing dependencies.json file in {base_dir}")

    with open(deps_path, "r") as file:
        rawdata = json.load(file)

    deps = rawdata.get("build-in-dependencies", [])

    for dep in deps:
        if dep == "os":
            useos = True
        elif not is_empty(dep):
            error.UnknowDependenciesError(f"Unknown dependency: {dep}")

    return useos
def is_true(condition,pc):
    
    if condition == "True":
        return True
    elif condition == "False":
        return False

    else:
        if not re.match(r'^[0-9\s\<\>\=\!\&\|\(\)]+$', condition):
            error.VauleError("Unsafe condition",pc)
        
        return eval(condition)        
def If(line,pc):
    n, text = line.split("if", 1)
    text=text.replace("{","",-1)
    condition = text.strip()
    return is_true(condition,pc)
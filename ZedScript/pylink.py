import os
import ZedScript.utils as utils
import ZedScript.error as error

def pylink_exec(python_code,stack_var,pc):
    pylink_env = {}
    exec("\n".join(python_code), pylink_env)
    variables = {k: v for k, v in pylink_env.items() if k != "__builtins__"}
    for name,value in variables.items(): 
        if name not in stack_var:    
            value_type = utils.check_type(str(value), pc)
            stack_var[name] = (value_type, value)
    
    return stack_var
def PyLink(line, stack_var, pc, base_dir=None):
    try:
        _, text = line.split("pylink", 1)
        filename = utils.get_string_context(text.strip())
        if not filename:
            raise error.SyntaxError("Missing filename in pylink statement", pc)
    except ValueError:
        raise error.SyntaxError("Invalid pylink syntax", pc)

    if base_dir:
        filepath = os.path.join(base_dir, filename)
    else:
        filepath = filename

    if not os.path.exists(filepath):
        raise error.ImportError(f"Linked Python file not found: {filepath}")

    python_code = utils.get_context(filepath)
    return pylink_exec(python_code, stack_var, pc)

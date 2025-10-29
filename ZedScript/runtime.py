import os
import re
import ZedScript.utils as utils
import ZedScript.error as error
import ZedScript.pylink as pylink
useos = False  
FILENAME=""
def execute(context: list):
    """Main interpreter loop that processes each line of the ZedScript file."""
    global useos
    global FILENAME
    stack_var = {}
    pc = 1 
    in_pyblock = False
    python_code=[]
    for line in context:

        line = str(line).strip()
        if utils.is_empty(line):
            pc += 1
            continue
        if in_pyblock:
            if line.startswith("endpy"):
                if in_pyblock == True:
                    if not python_code:
                        error.SyntaxError("python block was empty",pc)
                    else:
                        stack_var=pylink.pylink_exec(python_code,stack_var,pc)
                        in_pyblock=False
                        continue
                else:
                    error.SyntaxError("Never Enter a python block",pc)
            else:
                python_code.append(line)
            continue
        if line.startswith("py:"):
            in_pyblock = True
            python_code=[]
            continue
        if line.endswith(";"):
            line = line[:-1]
        elif not line.startswith("//"):
            error.SyntaxError("';' expected at end of line", line_number=pc)
        if line.startswith("pylink"):
            base_dir = os.path.dirname(os.path.abspath(FILENAME))
            stack_var = pylink.PyLink(line, stack_var, pc, base_dir)
            pc+=1
            continue
        for var_name, (var_type, var_value) in stack_var.items():
            pattern = rf"\b{re.escape(var_name)}\b"
            line = re.sub(pattern, str(var_value), line)
        
        if line.startswith("//"):
            pc += 1
            continue

        if line.startswith("input("):
            utils.Input(line, pc)
            pc += 1
            continue


        if line.startswith("var "):
            line = line.replace("var ", "", 1)
            name, value = line.split("=", 1)
            name, value = name.strip(), value.strip()

            var_type = utils.check_type(value, pc)

            if var_type == "math":
                value = utils.math(value,pc)
            elif var_type == "input":
                value = utils.Input(value, pc)
            elif var_type == "os.getcwd" and useos:
                value = utils.make_str(os.getcwd())

            stack_var[name] = (var_type, value)
            pc += 1
            continue

        if re.search(r"\b\d+\s*[\+\-\*/%]\s*\d+\b", line):
            expression = line
            result = utils.math(expression,pc)
            line = f'"{result}"'


        if line.startswith("print("):
            
            utils.Print(line, pc)
            pc += 1
            continue

        if "os.getcwd(" in line and useos:
            line = line.replace("os.getcwd()", os.getcwd())

        pc += 1


def run(filename: str):
    """Entry point for running a ZedScript file."""
    global useos
    global FILENAME
    useos = False 
    FILENAME=filename
    utils.check_dependencies(filename)

    context = utils.get_context(filename)

    execute(context)


if __name__ == "__main__":
    run("TEST/test.zs")

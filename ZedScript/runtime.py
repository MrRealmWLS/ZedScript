import os
import re
import ZedScript.utils as utils
import ZedScript.error as error
import ZedScript.pylink as pylink
useos = False  
FILENAME=""
def execute(context: list,stack_var={}):
    global useos, FILENAME
    pc = 0
    in_pyblock = False
    python_code = []
    block_stack = []
    last_block={}
    while pc < len(context):
        line = context[pc].strip()

        if utils.is_empty(line):
            pc += 1
            continue
        if line.endswith(";"):
            line=line.replace(";", "", -1)
            

        if in_pyblock:
            if line.startswith("endpy"):
                if not python_code:
                    error.SyntaxError("python block was empty", pc + 1)
                stack_var = pylink.pylink_exec(python_code, stack_var, pc + 1)
                in_pyblock = False
                python_code = []
                pc += 1
                continue
            else:
                python_code.append(line)
                pc += 1
                continue
        elif line.startswith("py:"):
            in_pyblock = True
            python_code = []
            pc += 1
            continue

        if line.startswith("pylink"):
            base_dir = os.path.dirname(os.path.abspath(FILENAME))
            stack_var = pylink.PyLink(line, stack_var, pc + 1, base_dir)
            pc += 1
            continue

        if block_stack and not all(b["active"] for b in block_stack):
            if line == "{":
                block_stack[-1]["inside_braces"] = True
            elif line.startswith("}") or line == "}":
                last_block=block_stack.pop()
                line=line.replace("}","",1)
            pc += 1
            continue
        if not line.startswith("var "):
            words_in_line = set(re.findall(r'\b\w+\b', line))
            for var_name, (var_type, var_value) in stack_var.items():
                if var_name in words_in_line:
                    pattern = utils.get_var_pattern(var_name)
                    line = re.sub(pattern, lambda m: str(var_value), line)

            
        if line.startswith("//"):
            pc += 1
            continue

        if line.startswith("input("):
            utils.Input(line, pc + 1)
            pc += 1
            continue

        if line.startswith("var "):
            line_content = line.replace("var ", "", 1)
            name, value = line_content.split("=", 1)
            name, value = name.strip(), value.strip()

            words_in_rhs = set(re.findall(r'\b\w+\b', value))
            for var_name, (var_type, var_value) in stack_var.items():
                if var_name in words_in_rhs:
                    pattern = utils.get_var_pattern(var_name)
                    value = re.sub(pattern, str(var_value), value)

            var_type = utils.check_type(value, pc + 1)
            if var_type == "math":
                value = utils.math(value, pc + 1)
            elif var_type == "input":
                value = utils.Input(value, pc + 1)
            elif var_type == "os.getcwd":
                if useos:
                    value = utils.make_str(os.getcwd())
                else:
                    error.ImportError("os module not imported. Add 'os' to dependencies.json to use os.getcwd()", pc + 1)

            stack_var[name] = (var_type, value)
            pc += 1
            continue

        if re.search(r"\b\d+\s*[\+\-\*/%]\s*\d+\b", line):
            result = utils.math(line, pc + 1)
            line = f'"{result}"'
            pc += 1
            continue

        if line.startswith("print("):
            utils.Print(line, pc + 1)
            pc += 1
            continue

        if line.startswith("if"):
            condition = utils.If(line, pc + 1)
            next_line = context[pc + 1] if pc + 1 < len(context) else ""
            if next_line.strip() == "{":
                pc += 1
            block_stack.append({"type": "if", "active": condition, "inside_braces": False})
            pc += 1
            continue
        if line.startswith("else"):
            if last_block != {} and last_block["type"] == "if":
                if not last_block["active"]:
                    next_line = context[pc + 1] if pc + 1 < len(context) else ""
                    if next_line.strip() == "{":
                        pc += 1
                    block_stack.append({"type": "else", "active": not last_block["active"], "inside_braces": False})
                    pc += 1
                    continue
            else:
                print(last_block)
                error.SyntaxError("Unexpected 'else'",pc+1)
                return
        if line.startswith("while"):
            condition = utils.While(line, pc + 1)
            next_line = context[pc + 1] if pc + 1 < len(context) else ""
            if next_line.strip() == "{":
                pc += 1
            
            block_stack.append({"type": "while", "active": condition,"start_pc": pc, "statement":line,"inside_braces": False})
            pc += 1
            continue


        if line == "}":
            if not block_stack:
                error.SyntaxError("Unexpected '}'", pc + 1)

            last_block = block_stack[-1]  

            if last_block["type"] == "while":
                active = utils.While(last_block["statement"], pc)
                if active:
                    pc = last_block["start_pc"] 
                    continue
                else:
                    block_stack.pop() 
            else:
                block_stack.pop()  

            pc += 1
            continue


        if "os.getcwd(" in line and useos:
            line = line.replace("os.getcwd()", os.getcwd())
            pc += 1
            continue
        print(line)
        error.SyntaxError(f"Invalid syntax {line}").zed_raise(pc + 1)
    return stack_var
def run(filename: str):
    """Entry point for running a ZedScript file."""
    global useos
    global FILENAME
    useos = False 
    FILENAME=filename
    useos=utils.check_dependencies(filename)

    context = utils.get_context(filename)

    execute(context)


if __name__ == "__main__":
    run("TEST/test.zs")

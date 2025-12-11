import sys
import ZedScript.runtime as runtime
try:
    filename=sys.argv[1]
except IndexError:
    stack_var={}
    while True:
        try:
            repl=input("[*] ZedScript > ")
            stack_var=runtime.execute(repl.splitlines(),stack_var)
        except KeyboardInterrupt:
            sys.exit()
runtime.run(filename)
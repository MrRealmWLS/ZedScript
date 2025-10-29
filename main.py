import sys
import ZedScript.runtime as runtime
try:
    filename=sys.argv[1]
except IndexError:
    print("""
Error: Program is terminated 
please used ZedScript.exe filename.zs """)
    sys.exit()
runtime.run(filename)
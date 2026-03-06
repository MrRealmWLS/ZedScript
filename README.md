<img src="https://github.com/MrRealmWLS/ZedScript/blob/main/zedscript_logo.png?raw=true" alt="logo" width="200"/>

# ZedScript

ZedScript is a lightweight scripting language with a direct interpreter no parsing phase, everything executes line by line. It supports variables, math operations, input/output, comments, and Python embedding via py: blocks, making it fast, simple, and seamlessly integrated with Python for flexible scripting.

## Installation

```bash
git clone https://github.com/MrRealmWLS/ZedScript.git
cd ZedScript
```

Requires Python 3.8+.

## Usage

run the command line:

```bash
python main.py <filename>
```

## Syntax

Comments:

```zs
// This is a comment
```

Variable declaration:

```zs
var x = 10;                  // Declare variable
var name = input("Enter name: ");  // Get user input
```

Printing output:

```zs
print("Hello " + name);
```

Math operations:

```zs
var result = 5 + 3 * 2;
```

Python blocks:

```zs
py:
    z = x + result
endpy
```

## Notes

* Every statement must end with a semicolon `;`.
* `Print()` displays text.
* `input()` reads user input.
* Use `py:` … `endpy` to execute Python code.

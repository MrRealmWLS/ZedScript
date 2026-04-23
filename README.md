<p align="center">
  <img src="https://github.com/RealmWLS/ZedScript/blob/main/zedscript_logo.png?raw=true" alt="ZedScript Logo" width="200"/>
</p>

<h1 align="center">ZedScript</h1>

<p align="center">
A scripting language with a direct interpreter built in Python.
</p>

---

## About

ZedScript is a programming language implemented in Python.  
It uses a direct interpreter where each line is executed at runtime without a separate compilation step.

It supports variables, math expressions, input/output, control flow, and Python embedding.

---

## Installation

```bash
git clone https://github.com/RealmWLS/ZedScript.git
cd ZedScript
````

Requirements:

* Python 3.8 or higher

---

## Usage

Run a ZedScript file:

```bash
python main.py <filename>
```

Example:

```bash
python main.py test.zs
```

---

## Syntax

### Comments

```zs
// This is a comment
```

### Variables

```zs
var x = 10;
var name = input("Enter your name: ");
```

### Output

```zs
print("Hello " + name);
```

### Math

```zs
var result = 5 + 3 * 2;
print(result);
```

### Python blocks

```zs
py:
    z = x + result
    print(z)
endpy
```

---

## Rules

* Every statement ends with `;`
* `print()` outputs text
* `input()` reads user input
* `py:` and `endpy` run Python code
* Execution uses a direct interpreter model

---

## Features

* Direct interpreter
* Variables and expressions
* Control flow (if, while)
* Python embedding

---

## Author

Created by RealmWLS

---

## Note

ZedScript is a programming language project made for learning interpreter and language design concepts.

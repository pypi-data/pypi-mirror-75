# Bysh

![tests](https://github.com/Haytek/bysh/workflows/tests/badge.svg)
![Upload Python Package](https://github.com/Haytek/bysh/workflows/Upload%20Python%20Package/badge.svg)

Bash interpreter in Python

Continuation of <https://github.com/idank/bashlex>. The bashlex files may have been modified.

## Installation

```shell
py -3 -m venv venv && venv/scripts/activate.bat
pip install bysh
bysh
```

## External libraries

Embedded in bysh.lib:
- [bashlex](https://github.com/idank/bashlex)
- [colorama](https://github.com/tartley/colorama)


## Notes

### alpha

For now the builtins and commands does not try to mimic the exact posix/bash behavior.
The goal is to have a working core, and then correct details.

### tkt

|| & && ; ;; ( ) | \n

- Simple Command
    - Noms separes par des espaces (+redirections) + control operator
- Pipeline
    - Simple commands séparées par des pipes
- List
    - pipelines séparées par des control operators
- Compound Commands
    - list mais avec des infos en plus
        - {} -> execute dans current shell
        - () -> execute subshell
        - (()) -> arithmetic
        - [[ ]] -> tests
- Shell functions
    - fonctions

### stdin

Plus tard il faudra  
msvcrt.getche() in (b'\x00', b'\xe0'):  
<https://docs.microsoft.com/en-us/cpp/c-runtime-library/reference/getch-getwch?view=vs-2019>

## TODO

Separate builtins from commands like $?

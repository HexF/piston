# Pistion Language Description File Format

## 16 Feburary 2021

This document outlines the PLD file format.
The format aims to unify the process of defining a language within the Piston Execution Engine into one simple file.
The format has been heavily inspired by the PKGBUILD format present in Arch Linux.


### Strucutre

The PLD file, at its core is a bash script containing functions and variables to do with the language and its lifecycle through piston.

A PLD File is always set for a specific version of an intepreter/language.
For example, when defining python, it should be posible to run Python 2.7, 3.7 and 3.8 all without conflict.

It is up to the discresion of the implementer to determine when to create a new language definition, but a general rule of thumb is on every breaking release (i.e. features get removed).

When interacting with the PLD file, it will be interpreted by bash and as such all bash features are at play.

The PLD is broken up into sections, and are required for each language unless specified.
Sections are either methods, variables or both, which should implement what is outlined for the specific language.

### Sections

#### Name

```
Name : name
Type : variable (string)
Chars: [a-z\.\-0-9]+
```

The name of the interpreter provided, and how it should be presented within piston.

The name should be kept lowercase and only include special characters `.` and `-` in the name.

Examples:

```bash
# Python 3.7
name="python3.7"

# NASM64
name="nasm64"
```

#### Version

```
Name : version
Type : method
Args : (none)
```

Returns the current version of the specified application in a SemVer compilant format

#### Aliases

```
Name : name
Type : variable (string[])
Chars: [a-z\.\-0-9]+
```

A list of names to accept as aliases when referring to this language in the context of execution.


#### Install

```
Name : install
Type : method
Args : (none)
```

A method containing all the commands to run to install the named interpreter.

The working directory when in the function will be located in `$PISTON_INSTALL/languages/$name` directory


#### Pre/Post Uninstall

```
Name : pre_uninstall
Name : post_uninstall
Type : method
Args : (none)
```

This method will be called before/after uninstallation of the interpreter.
It should be used for cleaning up any additional files that have been placed on the file system, outside of the regular language directory.

If the method is not required, it should be left as an empty function.

As in the `install` method, working directory is in `$PISTON_INSTALL/languages/$name`

During uninstallation the entire executer directory is removed, and the language is removed from the registry.

#### Compile

```
Name : compile
Type : method
Args : (none)
```

This method should compile source-code into a binary file and is called at execution time. It should only be used for languages which require AOT compilation (c/c++/rust) and not JIT compilation (python/jelly/osabie)

The method is given a 10 second timeout, failing immediately if the timelimit is exceeded

The working directory is a temp folder for the current execution, with code being available in the file `code.code`. The directory for `$PISTON_INSTALL/languages/$name` can be accessed through `$LBIN` (Language Binaries)

#### Run

```
Name : run
Type : method
Args : (none)
```

This method should execute the code using the specified runner.
It is given a 3 second timeout, failing if it times out.

The working directory is a temp folder for the current execution, with code being available in the file `code.code`, args in `args.args` seperated by `\n` bytes, and stdin data is available in `stdin.stdin`. The directory for `$PISTON_INSTALL/languages/$name` can be accessed through `$LBIN` (Language Binaries)

#### Path

```
Name : path
Type : method
Args : (none)
```

This method should return absolute paths to add to the $PATH variable.
This is called before execution, and should simply contain a handful of `echo` statements.

Like previous commands, the `$LBIN` variable is accessable.
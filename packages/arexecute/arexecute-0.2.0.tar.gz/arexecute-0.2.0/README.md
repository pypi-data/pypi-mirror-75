# arexecute
Application to record actions on the computer and then execute them in a controlled way.

## Installation

arexecute is in pypi, run the following command to install:

`python -m pip install arexecute`

After installation, all commands that are run using the module as a direct application can be run using either one of the following commands:

`python -m arexecute <arexecute-commands>`

or:

`arexecute <arexecute-commands>`

For the examples we will stick to the second one.

## Recording

To record into a file named "example.json", run the following line:

`arexecute example`

Here "example" can be a filename with a path different from the current directory,
or it can be only a filename, either with the .json extension or without it.
<br>
The instructions for recording are the following:

(->) Denotes press first one key, then the next
| Command                              | Action                                                       |
|--------------------------------------|--------------------------------------------------------------|
| Alt                                  | Stop recording                                               |
| W -> any number -> W                 | Add waiting time of seconds equal to the number              |
| Caps Lock -> any string -> Caps Lock | Writes the string                                            |
| Ctrl                                 | Move mouse to current mouse position                         |
| Shift n times                        | Clicks n times in the last mouse position determined by Ctrl |
| v                                    | Adds a variable to be defined later                          |
<br/>
In this way, one can record mouse movements, clicks, writing variables, etc.

## Executing

To execute, run the following line:

`arexecute example -e`

This will execute the recorded example once. In order to run more than one time, add an integer after de -e flag.
To run it indefinitely use the -r flag. In order for this command to work, a previous recording named "example.json" in the same
directory, or in the one specified by the filename must exist.

## Using Variables

When recording, typing 'v' will add a new variable in place. In order to define this variable, you can go to the json file, 'variable' key
and replace the "var_placeholder" strings for the variable itself. In order to use different variables for different iterations, replace
the same strings by lists of variables.

## Usage on a .py file

To use this program in a python script, just import the functions start_recording
and start_executing, this functions receive the file to execute/record to, and also
other parameters associated that are analogous to the flags shown.


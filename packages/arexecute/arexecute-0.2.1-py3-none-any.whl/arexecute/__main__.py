import argparse
import json
import sys

from .core import RecorderExecuter, start_executing, start_recording


INSTRUCTIONS ="""(->) Denotes press first one key, then the next
                  Alt                - Stop recording
         W -> any number -> W        - Add waiting time of seconds equal to the number
Caps Lock -> any string -> Caps Lock - Writes the string
                  Ctrl               - Move mouse to current mouse position
            Shift n times            - Clicks n times in the last mouse position determined by Ctrl
                  v                  - Adds a variable to be defined later
"""

def main():
    parser = argparse.ArgumentParser(description="Record/Execute keyboard and mouse actions.", prog="Recorder/Executer")

    parser.add_argument("filename", action="store", help="Filename to be used for execution/recording (with or without extension, can be a full path).")
    parser.add_argument("-e", nargs="?", const=1, action="store", dest="execute", type=int, help="Sets the execution mode on with i iterations (defaults to 1 iteration when number not specified).")
    parser.add_argument("-r", action="store_true", dest="recursively", default=False, help="Runs the execution recursively until process killed. No effect on recording.")
    parser.add_argument("-a", action="store", default=None, dest="after_script", help="Sets a python script to be executed after the actions (without .py extension).")

    args = parser.parse_args()

    print("\n========================ACTION RECORD EXECUTE========================\n")

    json_filename = args.filename

    execute = args.execute is not None
    iterations = args.execute

    if execute:
        start_executing(json_filename, ask_before=True, iterations=iterations, after_script=args.after_script, recursively=args.recursively)

    else:
        start_recording(json_filename, ask_before=True)

    input("Process finished successfully, press enter to leave...\n")


if __name__ == "__main__":
    main()

import time
from pathlib import Path

from ..keyutils import KeyPressWrapper, KeySet
from .recorder_executer import RecorderExecuter


INSTRUCTIONS ="""(->) Denotes press first one key, then the next
                  Alt                - Stop recording
         W -> any number -> W        - Add waiting time of seconds equal to the number
Caps Lock -> any string -> Caps Lock - Writes the string
                  Ctrl               - Move mouse to current mouse position
            Shift n times            - Clicks n times in the last mouse position determined by Ctrl
                  v                  - Adds a variable to be defined later
"""


def start_recording(record_file, ask_before=False):
    recorder = RecorderExecuter(record_file, execute=False)

    run(recorder, False, ask_before=ask_before)


def start_executing(execute_file, ask_before=False, iterations=1, after_script=None, recursively=False):
    executer = RecorderExecuter(execute_file, execute=True, iterations=iterations, after_script=after_script)

    run(executer, True, ask_before=ask_before, recursively=recursively)


def run(recorder_executer, execute, ask_before=False, recursively=False):

    if ask_before:
        msg = f"{INSTRUCTIONS}\nPress enter to start recording... (to leave just write exit and then enter)" if not execute else "Press enter to start executing... (to leave just write exit and then enter)"
        start = input(msg)

        if start == "exit":
            exit("Program stopped by the user.")

        else:
            print("Recording..." if not execute else "Executing...")

    else:
        print(f"Started {'executing' if execute else 'recording'}")

    recorder_executer.setUp()
    recorder_executer.start()

    if execute and recursively:
        while True:
            recorder_executer.start()


def write(text):
    print("Writing")
    keyboard = KeyPressWrapper()
    keyboard.press_release(list(map(lambda x: str(x), text)))
    time.sleep(0.2)

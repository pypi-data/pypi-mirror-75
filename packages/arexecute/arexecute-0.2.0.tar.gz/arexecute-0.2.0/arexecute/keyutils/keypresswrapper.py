from pynput.keyboard import Controller, KeyCode


class KeyPressWrapper:
    def __init__(self):
        self._keyboard = Controller()

    def hold_on(self, keys):
        for key in keys:
            self._keyboard.press(key)

    def hold_off(self, keys):
        for key in keys:
            self._keyboard.release(key)

    def press_release(self, keys):
        self.hold_on(keys)
        self.hold_off(keys)

    @staticmethod
    def keyToKeyCodePair(key):
        try:
            return int(key.value.vk), KeyCode(int(key.value.vk)), True

        except AttributeError:
            return str(key.char), KeyCode(char=str(key.char)), False

    @staticmethod
    def intStrToKeyCode(key):
        try:
            return KeyCode(int(key))

        except ValueError:
            return KeyCode(char=key)

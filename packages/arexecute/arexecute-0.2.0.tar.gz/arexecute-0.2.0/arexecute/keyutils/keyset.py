from .keypresswrapper import KeyPressWrapper


class KeySet:
    def __init__(self):
        self._keys_pressed = []
        self._is_combination = False

    def holdKey(self, key, alpha=True, special=True):
        key_pair = KeyPressWrapper.keyToKeyCodePair(key)
        if len(self._keys_pressed) >= 1 and not key_pair[2]:
            self._is_combination = True
        if (alpha and not key_pair[2]) or (special and key_pair[2]):
            self._keys_pressed.append((key_pair[0], key_pair[2]))
        return not key_pair[2]

    def releaseKey(self, key, alpha=True, special=True):
        key_pair = KeyPressWrapper.keyToKeyCodePair(key)
        if ((alpha and not key_pair[2]) or (special and key_pair[2])) and ((key_pair[0], key_pair[2]) in self._keys_pressed):
            self._keys_pressed.remove((key_pair[0], key_pair[2]))
        return not key_pair[2]

    def toArray(self):
        return [key for key, key_type in self._keys_pressed].copy()

    def isCombination(self):
        return self._is_combination

    def reset(self):
        self._keys_pressed = []
        self._is_combination = False
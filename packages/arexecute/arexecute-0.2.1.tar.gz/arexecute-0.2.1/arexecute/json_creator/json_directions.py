import json
from collections import deque


class JsonDirections:
    def __init__(self, translations):
        self._json_template = {"Recordings": [{
            "directions_order": [],
            "move": [],
            "click": []
        }]}
        self._inverted_translations = {v: k for k, v in translations.items()}
        self._stacks = {"directions_order": deque([])}

        for value in translations.values():
            self._stacks[value] = deque([])

    def push(self, direction_type, direction):
        self._stacks[direction_type].append(direction)
        self._stacks["directions_order"].append(self._inverted_translations[direction_type])

    def toJson(self):
        for key, adeque in self._stacks.items():
            self._json_template["Recordings"][0][key] = list(adeque)

        return self._json_template

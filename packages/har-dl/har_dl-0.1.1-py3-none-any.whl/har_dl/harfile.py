import json
from typing import List


class HARFile:
    def __init__(self, path: str):
        self.path = path
        self.json = None

    def load(self) -> None:
        with open(self.path, "r") as har:
            data = har.read()
            self.json = json.loads(data)

    @property
    def entries(self) -> List[str]:
        return [
            entry["request"]["url"] for entry in self.json["log"]["entries"]
            if entry["request"]["method"] == "GET"
        ]

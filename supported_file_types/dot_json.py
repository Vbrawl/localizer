import json
from localizer.FileHandler import FileHandler

class FHandler(FileHandler):
    @staticmethod
    def parse(file:str) -> dict[str, str] | set[str]:
        with open(file, 'r', encoding="utf-8") as f:
            out = json.load(f)
            if isinstance(out, list):
                return set(out)
            else:
                return out

    @staticmethod
    def export(file:str, texts:dict[str, str] | set[str]) -> None:
        with open(file, 'w', encoding="utf-8") as f:
            if isinstance(texts, set):
                json.dump(list(texts), f)
            else:
                json.dump(texts, f)
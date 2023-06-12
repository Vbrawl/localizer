import json

class FHandler():#FileHandler):
    @staticmethod
    def parse(file:str) -> dict[str, str]:
        with open(file, 'r') as f:
            return json.load(f)

    @staticmethod
    def export(file:str, texts:dict[str, str] | set[str]) -> None:
        with open(file, 'w') as f:
            json.dump(texts, f)
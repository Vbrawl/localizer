class FileHandler:
    @staticmethod
    def parse(file:str) -> dict[str, str]:
        raise NotImplementedError("This method must be overridden")
    
    @staticmethod
    def export(file:str, texts:dict[str, str] | set[str]) -> None:
        raise NotImplementedError("This method must be overridden")
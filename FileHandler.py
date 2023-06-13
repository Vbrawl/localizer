class FileHandler:
    @staticmethod
    def parse(file:str) -> dict[str, str] | set[str]:
        """A function to parse a file and extract it's data.

        Args:
            file (str): The filepath/filename of the file to process.

        Raises:
            NotImplementedError: This is always raised when calling FileHandler.parse, you should call the `parse` method of the child classes.

        Returns:
            dict[str, str]: A dictionary with key: value pairs where key is the `original text` and value is the `translated text`, or a set where each value is an `original text` where there is no translation for it.
        """
        raise NotImplementedError("This method must be overridden")
    
    @staticmethod
    def export(file:str, texts:dict[str, str] | set[str]) -> None:
        """A function to export the `texts` to a file.

        Args:
            file (str): The filepath/filename to the file which will hold the data. (The file is created if it doesn't exist).
            texts (dict[str, str] | set[str]): A dictionary with key: value pairs where key is the `original text` and value is the `translated text`, or a set where each value is an `original text` where there is no translation for it.

        Raises:
            NotImplementedError: This is always raised when calling FileHandle.export, you should call the `export` method of the child classes.
        """
        raise NotImplementedError("This method must be overridden")
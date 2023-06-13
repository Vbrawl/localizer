from typing import Optional
from localizer.FileHandler import FileHandler
from localizer.supported_file_types import FILE_TYPES

class LanguagePack:
    def __init__(self):
        self.o_t:dict[str, str] = dict()                            # original: translated
        self.new_texts:set[str] = set()
        self.supported_file_types:dict[str, type[FileHandler]] = dict()   # extension: FileHandler

        for ext, fhandler in FILE_TYPES.items():
            self.set_file_extension(ext, fhandler)

    def set_file_extension(self, extension:str, fhandler:type[FileHandler]):
        """Creates a connection between the specified `extension` and the specified `FileHandler`
        which allows to later process files of that extension with the correct `FileHandler`.

        Args:
            extension (str): The extension of the file that the Handler can process (Example, .json, .csv).
            fhandler (type[FileHandler]): A reference to the class holding the static methods for parsing and exporting the files.
        """

        if not extension.startswith('.'):
            extension = '.' + extension
        self.supported_file_types[extension] = fhandler

    def export_file(self, file:str) -> None:
        """Exports the data of the language pack to the specified `file`.
        The data is processed and stored using the `FileHandler` for the specific file format.

        Args:
            file (str): A string with the filepath/filename of the file. (The file will be created if it doesn't exist).
        """

        for extension, fhandler in self.supported_file_types.items():
            if file.endswith(extension):
                new_texts_file = file[:-len(extension)]+'.new_text'+extension
                fhandler.export(file, self.o_t)
                if self.new_texts: # is not empty:
                    fhandler.export(new_texts_file, self.new_texts)
                return # Return as soon as you export the file(s)

    def parse_file(self, file:str) -> None:
        """Parses the data of `file` and stores them in the language pack.
        The data is processed and stored using the `FileHandler` for the specific file format.

        Args:
            file (str): A string with the filepath/filename of the file.

        Raises:
            TypeError: If there is no handler available to process this file.
        """
        o_t:Optional[dict[str, str] | set[str]] = None
        for extension, fhandler in self.supported_file_types.items():
            if file.endswith(extension):
                o_t = fhandler.parse(file)
                break # Continue as soon as you process the file(s)
        if o_t is None:
            raise TypeError("File must end with one of the following extensions: " + ', '.join(self.supported_file_types.keys()))

        if isinstance(o_t, dict):
            for o, t in o_t.items():
                self.o_t[o] = t
                try:
                    self.new_texts.remove(o)
                except KeyError:
                    pass # o doesn't exist to begin with.
        else:
            for o in o_t:
                if o not in self.o_t.keys():
                    self.new_texts.add(o)
    
    def add_translation(self, original:str, translated:str) -> None:
        """Add a translation for a sentence in the language pack.

        Args:
            original (str): The original sentence.
            translated (str): The translated sentence.
        """
        self.o_t[original] = translated
        if original in self.new_texts:
            self.new_texts.remove(original)
    
    def gettext(self, text:str) -> str:
        """Get the translation of `text` if it exists,
        otherwise fallback to the original translation.

        Args:
            text (str): The text to be translated.

        Returns:
            str: The translated text, or the original text (If no translation was found).
        """
        if text == '' or text in self.new_texts:
            return text
        elif text in self.o_t.keys():
            return self.o_t[text]
        else:
            self.new_texts.add(text)
            return text
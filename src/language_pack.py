from typing import Callable, Optional
from FileHandler import FileHandler #TODO: Add full path

class LanguagePack:
    def __init__(self):
        self.o_t:dict[str, str] = dict()                            # original: translated
        self.new_texts:set[str] = set()
        self.supported_file_types:dict[str, FileHandler] = dict()   # extension: FileHandler

        #from localizer.src.supported_file_types import dot_csv, dot_json
        from supported_file_types import dot_csv, dot_json
        self.set_file_extension('.csv', dot_csv.FHandler())
        self.set_file_extension('.json', dot_json.FHandler())

    def set_file_extension(self, extension:str, fhandler:FileHandler):
        if not extension.startswith('.'):
            extension = '.' + extension
        self.supported_file_types[extension] = fhandler

    def export_file(self, file:str) -> None:
        for extension, fhandler in self.supported_file_types.items():
            if file.endswith(extension):
                new_texts_file = file[:-len(extension)]+'.new_text'+extension
                fhandler.export(file, self.o_t)
                fhandler.export(new_texts_file, self.new_texts)

    def parse_file(self, file:str) -> None:
        o_t:Optional[dict[str, str]] = None
        for extension, fhandler in self.supported_file_types.items():
            if file.endswith(extension):
                o_t = fhandler.parse(file)
        if o_t is None:
            raise TypeError("File must end with one of the following extensions: " + ', '.join(self.supported_file_types.keys()))

        for o, t in o_t.items():
            self.o_t[o] = t
            try:
                self.new_texts.remove(o)
            except KeyError:
                pass # o doesn't exist to begin with.
    
    def add_translation(self, original:str, translated:str) -> None:
        self.o_t[original] = translated
    
    def gettext(self, text:str) -> str:
        if text == '' or text in self.new_texts:
            return text
        elif text in self.o_t.keys():
            return self.o_t[text]
        else:
            self.new_texts.add(text)
            return text
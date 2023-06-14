from typing import Optional
import translators as ts
from localizer.FileHandler import FileHandler
from localizer.supported_file_types import FILE_TYPES
import asyncio

def count_spaces(text:str) -> int:
            for i, v in enumerate(text, 1):
                if v != ' ':
                    return i-1
            return 0


class LanguagePack:
    def __init__(self):
        self.o_t:dict[str, str] = dict()                                    # original: translated
        self.new_texts:set[str] = set()
        self.supported_file_types:dict[str, type[FileHandler]] = dict()     # extension: FileHandler
        self.translate_from_language = "auto"
        self.translate_to_language = "en"
        self.translators = ["deepl", "google", "bing"]
        self.translator_tries = 5
        self.auto_translate = False

        for ext, fhandler in FILE_TYPES.items():
            self.set_file_extension(ext, fhandler)
    
    def translate_all(self):
        """Asynchronously translate all `new_texts` and store them in the pack.

        NOTE: The options are the LanguagePack's attributes `self.translat*`
        """
        loop = asyncio.new_event_loop()
        results:dict[str, asyncio.Future[str]] = {}
        for original in self.new_texts:
            #                                                              query_text, to_language, from_language, translators, tries, auto_add
            results[original] = loop.run_in_executor(None, self.translate, original,   None,        None,          None,        None,  False)

        gather = asyncio.gather(*results.values(), return_exceptions=True)
        loop.run_until_complete(gather)
        for original in results.keys():
            translated = results[original].result()
            self.add_translation(original, translated)

    def translate(self, query_text:str, to_language:Optional[str] = None, from_language:Optional[str] = None, translators:Optional[list[str]] = None, tries:Optional[int] = None, auto_add:bool = True) -> Optional[str]:
        """Translate `query_text` from `from_language` to `to_language` using one of the `translators` (starting from the first and using the others as fallbacks).
        You also have the option to automatically add the translation to the pack (if the translation succeeds) using `auto_add=True`

        Args:
            query_text (str): The original text to translate.
            to_language (Optional[str], optional): The code of the language for the translated text. Defaults to None.
            from_language (Optional[str], optional): The code of the language for the original text (or `auto`). Defaults to None.
            translators (Optional[list[str]], optional): A list of translators to use (first is primary and the others are fallbacks). Defaults to None.
            tries (Optional[int], optional): How many tries before going to the next translator. Defaults to None.
            auto_add (bool, optional): Wether to add the translation to the pack or return it to the program. Defaults to True.

        Returns:
            Optional[str]: If `auto_add` is True the return value is None, if `auto_add` is False the return value is the translated text.
        """
        if not to_language:
            to_language = self.translate_to_language
        if not from_language:
            from_language = self.translate_from_language
        if not translators:
            translators = self.translators
        if not tries:
            tries = self.translator_tries

        start_spaces = count_spaces(query_text)
        end_spaces = count_spaces(query_text[::-1])
        query_text = query_text[start_spaces:]

        if end_spaces != 0:
            query_text = query_text[:-end_spaces]

        for translator in translators:
            for i in range(tries):
                try:
                    translated = (' ' * start_spaces) + ts.translate_text(query_text=query_text, translator=translator, from_language = from_language, to_language = to_language) + (' ' * end_spaces) # type: ignore
                    if auto_add:
                        self.add_translation(query_text, translated)
                    else:
                        return translated
                except Exception:
                    pass

    def get_file_extension(self, filename:str) -> Optional[str]:
        """Finds and returns the extension of the file ONLY if that extension is supported.

        Args:
            filename (str): The name of the file.

        Returns:
            Optional[str]: The extension of the file (if the extension is supported), or None (if the extension is NOT supported).
        """
        for k in self.supported_file_types.keys():
            if filename.endswith(k):
                return k
        return None

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
        extension = self.get_file_extension(file)
        if not extension:
            raise TypeError("File must end with one of the following extensions: " + ', '.join(self.supported_file_types.keys()))
        fhandler = self.supported_file_types[extension]
        new_texts_file = file[:-len(extension)]+'.new_text'+extension

        fhandler.export(file, self.o_t)
        if self.new_texts:
            fhandler.export(new_texts_file, self.new_texts)

    def parse_file(self, file:str) -> None:
        """Parses the data of `file` and stores them in the language pack.
        The data is processed and stored using the `FileHandler` for the specific file format.

        Args:
            file (str): A string with the filepath/filename of the file.

        Raises:
            TypeError: If there is no handler available to process this file.
        """
        extension = self.get_file_extension(file)
        if not extension:
            raise TypeError("File must end with one of the following extensions: " + ', '.join(self.supported_file_types.keys()))
        fhandler = self.supported_file_types[extension]
        o_t = fhandler.parse(file)
        if isinstance(o_t, set):
            o_t = map(lambda x: (x,''), o_t)
        elif isinstance(o_t, dict):
            o_t = o_t.items()
        for o, t in o_t:
            self.add_translation(o, t)

    
    def add_translation(self, original:str, translated:Optional[str] = None) -> None:
        """Add a translation for a sentence in the language pack.
        If the translated text is empty, original is added to new_texts.

        If `self.auto_translate` is True, an attempt to automatically translate
        the original using a translator API is made.

        Args:
            original (str): The original sentence.
            
            translated (Optional[str], optional): The translated sentence. Defaults to None
        """
        if translated:
            self.o_t[original] = translated
            try:
                self.new_texts.remove(original)
            except KeyError:
                pass # original doesn't exist anyway.
        else:
            self.new_texts.add(original)
            if self.auto_translate: self.translate(original)
    
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
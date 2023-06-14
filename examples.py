def supported_file_extensions():
    """In the source code of this function you will find how to view
    all supported_file_extensions as well as how to add support for
    other file_extensions.
    """
    from localizer import GLOBAL_LANGUAGE_PACK

    # view supported file extensions
    print(GLOBAL_LANGUAGE_PACK.supported_file_types.keys())


    # add support for (example) json
    import json
    from localizer.FileHandler import FileHandler
    class JSONFHandler(FileHandler):
        @staticmethod
        def parse(file:str) -> dict[str, str] | set[str]:
            with open(file) as f:
                data = json.load(file)
            
            if isinstance(data, dict):
                # original: translated
                return data
            elif isinstance(data, list):
                # This is a special case where the file contains new_texts
                # where they don't have a translated version yet.
                return set(data)
        
        @staticmethod
        def export(file:str, texts:dict[str, str] | set[str]) -> None:
            with open(file, 'w') as f:
                if isinstance(texts, set):
                    texts = list(texts)
                # write either a dict or a list(derived from a set) to the file(f)
                json.dump(texts, f)
    
    # Register the type to the language pack.
    GLOBAL_LANGUAGE_PACK.set_file_extension(".json", JSONFHandler)





def using_a_language_pack():
    """In the source code of this function you will find information on
    how to use a language pack object.
    """
    from localizer.language_pack import LanguagePack

    lp = LanguagePack()

    #lp.parse_file("file.ext")  # Load translation pack
    lp.add_translation("Hello World", "Γειά σου Κόσμε") # Manually add a translation

    print(lp.gettext("Hello World")) # Output: Γειά σου Κόσμε
    #lp.export_file("file.ext") # Export Translation Pack to a file


def easy_mode():
    """In the source code of this function you will find information on
    how to use this library in easy mode.
    """
    from localizer import print, input, GLOBAL_LANGUAGE_PACK

    GLOBAL_LANGUAGE_PACK.add_translation("Hello World", "Γειά σου Κόσμε")
    GLOBAL_LANGUAGE_PACK.add_translation("Hello Suzan", "Γειά σου Σούζαν")
    GLOBAL_LANGUAGE_PACK.add_translation("How are you?", "Πώς είσαι;")

    print("Hello World") # Output: Γειά σου Κόσμε
    print("Hello Suzan") # Output: Γειά σου Σούζαν
    print("Hello World", "Hello Suzan") # Output: Γειά σου Κόσμε Γειά σου Σούζαν

    input("How are you?") # Output: Πώς είσαι; <Waiting for keyboard input>

    # NOTE that the following will not work
    input("Hello World Hello Suzan") # Output: Hello World Hello Suzan <Waiting...>

    # to fix the above you can do:
    _ = GLOBAL_LANGUAGE_PACK.gettext
    input(_("Hello World") + ' ' + _("Hello Suzan")) # Output: Γειά σου Κόσμε Γειά σου Σούζαν


def translation_using_APIs():
    """In the source code of this function you will find information on
    how to use translate texts using web APIs.
    """
    from localizer import GLOBAL_LANGUAGE_PACK

    GLOBAL_LANGUAGE_PACK.translate_from_language = "auto" # You can also enter a country code, ex: el, en, de and more.
    GLOBAL_LANGUAGE_PACK.translate_to_language = "el" # You can ONLY enter a country code.
    GLOBAL_LANGUAGE_PACK.translators = ["deepl", "google", "bing"] # They are used in order as fallbacks. You can enter as many translator APIs as you want, they need to be supported by the `translators` library
    GLOBAL_LANGUAGE_PACK.translator_tries = 5 # How many tries before falling back to another translator.

    ret = GLOBAL_LANGUAGE_PACK.translate("Hello World") # Translate using the settings specified above and ADD the translation to the language pack.
    print(ret) # None
    ret = GLOBAL_LANGUAGE_PACK.translate("Hello World", auto_add=False) # Translate using the settings specified above and DO NOT add the translation to the language pack.
    print(ret) # Translated version of "Hello World"

    # Translate using custom settings (You can ommit an option to use the global specified above)
    # ADD the translation to the language pack
    ret = GLOBAL_LANGUAGE_PACK.translate("Hello World", to_language="el", from_language="auto", translators=["deepl", "google", "bing"], tries=5)
    print(ret) # None

    # Same as above but DO NOT add the translation to the language pack
    ret = GLOBAL_LANGUAGE_PACK.translate("Hello World", to_language="el", from_language="auto", translators=["deepl", "google", "bing"], tries=5, auto_add=False)
    print(ret) # Translated version of "Hello World"


    # To batch translate texts
    GLOBAL_LANGUAGE_PACK.add_translation("Hello Suzan")
    GLOBAL_LANGUAGE_PACK.add_translation("Hello Jim")
    GLOBAL_LANGUAGE_PACK.add_translation("Hello Mike")

    # Uses asynchronous operations to translate everything. (WARNING: This will block the thread until every item is translated or errors out.)
    GLOBAL_LANGUAGE_PACK.translate_all()

    # OR you can enable automatic translation. (WARNING: This is slower and blocks program execution, you should NOT use it in production.)
    GLOBAL_LANGUAGE_PACK.auto_translate = True

    GLOBAL_LANGUAGE_PACK.add_translation("Hello Gwen") # Blocks until translation is complete
    GLOBAL_LANGUAGE_PACK.add_translation("Hello George") # Block until translation is complete
    GLOBAL_LANGUAGE_PACK.add_translation("Hello Bill") # Block until tranlsation is complete


def creating_language_packs():
    """You can use the `localizer_pack_fill.py` script to generate language packs.
    Run `localizer_pack_fill.py -h` for the help menu.
    """
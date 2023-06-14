import argparse, os, translators as ts
from localizer.language_pack import LanguagePack

def translate_text(query_text:str, from_language:str="auto", to_language:str="en", translators:list[str]=["deepl", "google", "bing"], tries=5) -> str:
    def count_spaces(text:str) -> int:
        for i, v in enumerate(text, 1):
            if v != ' ':
                return i-1
        return len(text)
    start_spaces = count_spaces(query_text)
    end_spaces = count_spaces(query_text[::-1])
    query_text = query_text[start_spaces:-end_spaces]

    for translator in translators:
        for i in range(tries):
            try:
                return (' ' * start_spaces) + ts.translate_text(query_text=query_text, translator=translator, from_language = from_language, to_language = to_language) + (' ' * end_spaces) # type: ignore
            except Exception:
                pass
    else:
        return ""


def get_translation(original:str, recommendation:str, prompt:str, qtranslator:bool = False):
    if qtranslator:
        return recommendation

    translated = input(prompt.format(original = original, recommendation = (" (" + recommendation + ")" if recommendation else "")))
    if recommendation and not translated:
        translated = recommendation
    return translated

parser = argparse.ArgumentParser(description="Create a language pack for the Python package `Localizer`.", add_help=True, exit_on_error=False)
parser.add_argument("language_pack_file", type=str, help="The language_pack file, this is going to be updated if it doesn't exist.")
parser.add_argument("--external_file", "-ef", type=str, nargs="*", help="Other language_packs(to get the original texts only), or new_texts files.")
parser.add_argument("--translator", "-t", action="store_true", help="Use a translator API to provide translation recommendations.")
parser.add_argument("--quick-translator", "-qt", action="store_true", help="Use a translator API to automatically translate everything. (Automated translation!)")
parser.add_argument("--from-lang", "-fl", type=str, default="auto", help="The language of the original text (language code).")
parser.add_argument("--to-lang", "-tl", type=str, help="The language of the translated text (language code).")

args = parser.parse_args()

lpf = args.language_pack_file
efs = args.external_file
translator = args.translator
qtranslator = args.quick_translator
fl = args.from_lang
tl = args.to_lang

lp = LanguagePack()

if lp.get_file_extension(lpf) is None:
    print("Error: Unsupported file extension.")
    print("Please select one of the following extensions: ")
    print(''.join(map(lambda x: f"\t* {x}\n", lp.supported_file_types.keys())))
    exit()

if translator and qtranslator:
    print("Error: Cannot enable translator and quick-translator at the same time.")
    exit()

if (translator or qtranslator) and not tl:
    print("Error: --to-lang needs to be specified.")
    exit()

if os.path.exists(lpf):
    lp.parse_file(lpf)

if efs:
    for f in efs:
        try:
            tmp_lp = LanguagePack()
            tmp_lp.parse_file(f)
            for o in tmp_lp.o_t.keys():
                if o not in lp.o_t.keys():
                    lp.new_texts.add(o)
            for nt in tmp_lp.new_texts:
                lp.new_texts.add(nt)
        except TypeError or PermissionError:
            print(f"Error: external_file({f}) doesn't exist. Ignoring...")

if lp.new_texts:
    print("First, please translate all the new_texts that were found:")
    new_texts = set(lp.new_texts)
    for nt in new_texts:
        recommendation = translate_text(nt, from_language=fl, to_language=tl) if (translator or qtranslator) else ""
        translated = get_translation(nt, recommendation, "{original}{recommendation} => ", qtranslator)
        if translated:
            lp.add_translation(nt, translated)

yes_NO = input("Would you like to add more texts? [yes/NO]: ")
print("When translation is empty, the original text enters the new_texts.")
print("Input an empty `original text` to finish adding texts.")
if yes_NO and yes_NO.upper() == "YES":
    cont = True
    while cont:
        original = input("Original Text: ")

        if original:
            recommendation = translate_text(original, from_language=fl, to_language=tl) if (translator or qtranslator) else ""
            translated = get_translation(original, recommendation, "Translated Text{recommendation}:", qtranslator)

            if translated:
                lp.add_translation(original, translated)
            else:
                lp.new_texts.add(original)
        else:
            cont = False

print("Saving Changes...")
lp.export_file(lpf)
print("Changes Saved.")
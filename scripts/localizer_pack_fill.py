import argparse, os
from localizer.language_pack import LanguagePack
from typing import Optional, Iterator

def get_translation(original:str, recommendation:Optional[str], prompt:str):
    translated = input(prompt.format(original = original, recommendation = (" (" + recommendation + ")" if recommendation else "")))
    if recommendation and not translated:
        translated = recommendation
    return translated

def get_next(it:Iterator[str]) -> Optional[str]:
    try:
        return next(it)
    except StopIteration:
        return None

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
lp.auto_translate = False
lp.translate_from_language = fl
lp.translate_to_language = tl

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

it = iter(lp.new_texts)
prompt = "{original}{recommendation} => "
iterator_ended = False
answer = False

while not iterator_ended or answer:
    if not iterator_ended:
        original = get_next(it)
    else:
        original = input("Original text: ")
    
    if original:
        recommendation = lp.translate(original, auto_add=False) if translator else None
        translated = get_translation(original, recommendation, prompt) if not qtranslator else None

        lp.add_translation(original, translated)
    elif not original and not iterator_ended:
        iterator_ended = True
        yes_NO = input("Would you like to add more texts? [yes/NO]: ")
        if yes_NO and yes_NO.upper() == "YES":
            print("To stop adding more texts, enter a blank original text.")
            print("You can add a new text by not providing a translation for an original text.")
            prompt = "Translated Text{recommendation}: "
            answer = True
    else:
        answer = False

if qtranslator:
    print("Translating All New Texts...")
    lp.translate_all()
    print("Translation Finished.")
print("Saving Changes...")
lp.export_file(lpf)
print("Changes Saved.")
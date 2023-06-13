import argparse, os
from localizer.language_pack import LanguagePack

parser = argparse.ArgumentParser(description="Create a language pack for the Python package `Localizer`.", add_help=True, exit_on_error=False)
parser.add_argument("language_pack_file", type=str, help="The language_pack file, this is going to be updated if it doesn't exist.")
parser.add_argument("--external_file", "-ef", type=str, nargs="*", help="Other language_packs(to get the original texts only), or new_texts files.")
#parser.add_argument("--translator", "-t", action="store_true", help="Use google translate to provide recommendations.")
#parser.add_argument("--quick-translator", "-qt", action="store_true", help="Use google translate to automatically translate everything. (Automated translation!)")

args = parser.parse_args()

lpf = args.language_pack_file
efs = args.external_file
#translator = args.translator
#qtranslator = args.quick_translator
translator = False      # NOT IMPLEMENTED
qtranslator = False     # NOT IMPLEMENTED

lp = LanguagePack()

if translator and qtranslator:
    print("Error: Cannot enable translator and quick-translator at the same time.")
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
            print("Error: external_file({f}) doesn't exist. Ignoring...")

if lp.new_texts:
    print("First, please translate all the new_texts that were found:")
    for nt in lp.new_texts:
        translated = input(f"{nt} => ")
        lp.add_translation(nt, translated)

yes_NO = input("Would you like to add more texts? [yes/NO]: ")
print("When translation is empty, the original text enters the new_texts.")
print("Input an empty `original text` to finish adding texts.")
if yes_NO and yes_NO.upper() == "YES":
    cont = True
    while cont:
        original = input("Original Text: ")

        if original:
            translated = input("Translated Text: ")

            if translated:
                lp.add_translation(original, translated)
            else:
                lp.new_texts.add(original)
        else:
            cont = False

print("Saving Changes...")
lp.export_file(lpf)
print("Changes Saved.")
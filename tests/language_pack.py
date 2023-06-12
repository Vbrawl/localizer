import unittest
import os
from localizer.language_pack import LanguagePack

REMOVE_GENERATED_FILES = True


class TestLanguagePack(unittest.TestCase):
    def test_export_parse(self):
        lp = LanguagePack()
        lp.add_translation("Hello World", "Γειά σου Κόσμε")
        lp.add_translation("Hello Suzan", "Γειά σου Σούζαν")

        file = os.path.join(os.getcwd(), "el.csv")
        lp.export_file(file)

        lp2 = LanguagePack()
        lp2.parse_file(file)

        if REMOVE_GENERATED_FILES: os.unlink(file)

        self.assertEqual(lp.gettext("Hello World"), lp2.gettext("Hello World"))


if __name__ == "__main__":
    unittest.main()
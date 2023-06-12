import os
import unittest
from localizer.supported_file_types.dot_csv import FHandler as CSVFHandler
from localizer.supported_file_types.dot_json import FHandler as JSONFHandler

REMOVE_GENERATED_FILES = True
csvfiles = {
    "normal": os.path.join(os.getcwd(), "csv_test.normal.csv"),
    "new_words": os.path.join(os.getcwd(), "csv_test.new_words.csv")
}

jsonfiles = {
    "normal": os.path.join(os.getcwd(), "json_test.normal.json"),
    "new_words": os.path.join(os.getcwd(), "json_test.new_words.json"),
}

class TestCSVFHandler(unittest.TestCase):

    def test_csv_export_parse_normal(self):
        export_payload = {
            "Hello World": "Γειά σου Κόσμε",
            "Hi Suzan": "Γειά σου Σούζαν"
        }
        CSVFHandler.export(csvfiles["normal"], export_payload)
        parsed_payload = CSVFHandler.parse(csvfiles["normal"])

        if REMOVE_GENERATED_FILES: os.unlink(csvfiles["normal"])

        self.assertEqual(export_payload, parsed_payload)
    
    def test_csv_export_parse_new_words(self):
        export_payload = set(["Hello World", "Hi Suzan"])
        CSVFHandler.export(csvfiles["new_words"], export_payload)
        parsed_payload = CSVFHandler.parse(csvfiles["new_words"])

        if REMOVE_GENERATED_FILES: os.unlink(csvfiles["new_words"])

        self.assertEqual(export_payload, parsed_payload)


class TestJSONFHandler(unittest.TestCase):

    def test_json_export_parse_normal(self):
        export_payload = {
            "Hello World": "Γειά σου Κόσμε",
            "Hi Suzan": "Γειά σου Σούζαν"
        }
        JSONFHandler.export(jsonfiles["normal"], export_payload)
        parsed_payload = JSONFHandler.parse(jsonfiles["normal"])

        if REMOVE_GENERATED_FILES: os.unlink(jsonfiles["normal"])

        self.assertEqual(export_payload, parsed_payload)
    
    def test_csv_export_parse_new_words(self):
        export_payload = set(["Hello World", "Hi Suzan"])
        JSONFHandler.export(jsonfiles["new_words"], export_payload)
        parsed_payload = JSONFHandler.parse(jsonfiles["new_words"])

        if REMOVE_GENERATED_FILES: os.unlink(jsonfiles["new_words"])

        self.assertEqual(export_payload, parsed_payload)




if __name__ == "__main__":
    unittest.main()
import csv
from localizer.FileHandler import FileHandler

class FHandler(FileHandler):
    @staticmethod
    def parse(file:str) -> dict[str, str]:
        o_t = {}
        with open(file, 'r') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                cr = len(row) # count row (column number)
                if cr > 0:
                    if row[0].startswith("[LP:IGNORE]"):
                        continue
                    elif cr >= 2:
                        o_t[row[0]] = row[1]
        return o_t

    @staticmethod
    def export(file:str, texts:dict[str, str] | set[str]) -> None:
        with open(file, 'w') as f:
            csv_writer = csv.writer(f)
            if isinstance(texts, dict):
                header = ('[LP:IGNORE] ORIGINAL', 'TRANSLATED')
                text_map = texts.items()
            else:
                header = ('[LP:IGNORE] NEW TEXTS')
                text_map = map(lambda x: (x,), texts)
            csv_writer.writerow(header)
            csv_writer.writerows(text_map)

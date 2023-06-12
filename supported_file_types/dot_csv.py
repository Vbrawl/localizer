import csv
from localizer.FileHandler import FileHandler

class FHandler(FileHandler):
    @staticmethod
    def parse(file:str) -> dict[str, str] | set[str]:
        o_t = {}
        cast_to_set = True
        with open(file, 'r', newline='') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                cr = len(row) # count row (column number)
                if cr > 0:
                    if row[0].startswith("[LP:IGNORE]"):
                        continue
                    elif cr >= 2:
                        o_t[row[0]] = row[1] # Here we have a dictionary
                        cast_to_set = False
                    else: # cr == 1
                        o_t[row[0]] = row[0] # Here we have a set (Don't update cast_to_set)
        if cast_to_set:
            o_t = set(o_t.keys())
        return o_t

    @staticmethod
    def export(file:str, texts:dict[str, str] | set[str]) -> None:
        with open(file, 'w', newline='') as f:
            csv_writer = csv.writer(f)
            if isinstance(texts, dict):
                header = ('[LP:IGNORE] ORIGINAL', 'TRANSLATED')
                text_map = texts.items()
            else:
                header = ('[LP:IGNORE] NEW TEXTS',)
                text_map = map(lambda x: (x,), texts)
            csv_writer.writerow(header)
            csv_writer.writerows(text_map)

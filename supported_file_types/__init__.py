from localizer.supported_file_types import dot_csv, dot_json
from FileHandler import FileHandler

FILE_TYPES:dict[str, type[FileHandler]] = {
    ".csv": dot_csv.FHandler,
    ".json": dot_json.FHandler
}
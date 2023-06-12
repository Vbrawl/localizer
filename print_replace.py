from io import TextIOWrapper
import sys
from typing import Optional, TextIO
from localizer.language_pack import LanguagePack

PRINT_LANGUAGE_PACK = LanguagePack() # An empty language pack to avoid errors.

def print(*values: object, sep:Optional[str] = ' ', end:Optional[str] = '\n', file:Optional[TextIOWrapper | TextIO] = None, flush:bool = False) -> None:
    generate_error_message = lambda name, value: f"{name} must be None or a string, not {' '.join(str(type(value)).split(' ')[1:])[1:-2]}"
    if not isinstance(sep, str) and sep is not None:
        raise TypeError(generate_error_message("sep", sep))
    elif not isinstance(end, str) and end is not None:
        raise TypeError(generate_error_message("end", end))

    if file is None:
        file = sys.stdout

    rendered_text = (sep or '').join(  map(lambda x: PRINT_LANGUAGE_PACK.gettext(x) if isinstance(x, str) else str(x), values)  ) + str(end or '')
    lrt = len(rendered_text)    # length rendered text
    wtl = 0                     # written text length

    while wtl < lrt:
        wtl += file.write(rendered_text[wtl:])
    
    if flush:
        file.flush()
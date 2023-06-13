import sys
from typing import Optional, IO
from localizer.language_pack import LanguagePack

PRINT_LANGUAGE_PACK = LanguagePack() # An empty language pack to avoid errors.

def print(*values: object, sep:Optional[str] = ' ', end:Optional[str] = '\n', file:Optional[IO] = None, flush:bool = False) -> None:
    """An emulated version of the default `print`.
    Allows `localizer` module to intercept the values passed to `print`
    and provide an easy way to translate them to different languages.

    Args:
        sep (Optional[str], optional): The separator, a value that's placed between the values. Defaults to ' '.
        end (Optional[str], optional): The ending value, a value that's placed at the end of the whole value list. Defaults to '\n'.
        file (Optional[IO], optional): The file object in which to write the buffer, None is replaced with STDOUT. Defaults to None.
        flush (bool, optional): Wether to flush the buffer or not. Defaults to False.

    Raises:
        TypeError: If `sep` is not of type `str` and not `None`.
        TypeError: If `end` is not of type `str` and not None.
    """

    # Shortcut for generating error messages.
    generate_error_message = lambda name, value: f"{name} must be None or a string, not {' '.join(str(type(value)).split(' ')[1:])[1:-2]}"

    # Check variable types and place default values.
    if not isinstance(sep, str) and sep is not None:
        raise TypeError(generate_error_message("sep", sep))
    elif sep is None:
        sep = ' '

    if not isinstance(end, str) and end is not None:
        raise TypeError(generate_error_message("end", end))
    elif end is None:
        end = '\n'

    if file is None:
        file = sys.stdout

    # Write everything one-by-one, then the end and then flush if required.
    for i, v in enumerate(values):
        if i != 0:
            file.write(sep)
        if isinstance(v, str):
            v = PRINT_LANGUAGE_PACK.gettext(v)
        else:
            v = str(v)
        file.write(v)
    file.write(end)

    if flush:
        file.flush()
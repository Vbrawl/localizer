import sys
from typing import Optional, IO
from localizer.language_pack import LanguagePack

GLOBAL_LANGUAGE_PACK = LanguagePack() # An empty language pack to avoid errors.

_print=print
def print(*values: object, sep:Optional[str] = ' ', end:Optional[str] = '\n', file:Optional[IO] = None, flush:bool = False) -> None:
    """An emulated version of the default `print`.
    Allows `localizer` module to intercept the values passed to `print`
    and provide an easy way to translate them to different languages.

    Args:
        sep (Optional[str], optional): The separator, a value that's placed between the values. Defaults to ' '.

        end (Optional[str], optional): The ending value, a value that's placed at the end of the whole value list. Defaults to '\\\\n'.

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
    else: # sep is str
        sep = GLOBAL_LANGUAGE_PACK.gettext(sep)

    if not isinstance(end, str) and end is not None:
        raise TypeError(generate_error_message("end", end))
    elif end is None:
        end = '\n'
    else: # end is str
        end = GLOBAL_LANGUAGE_PACK.gettext(end)

    if file is None:
        file = sys.stdout

    # Write everything one-by-one, then the end and then flush if required.
    for i, v in enumerate(values):
        if i != 0:
            file.write(sep)
        if isinstance(v, str):
            v = GLOBAL_LANGUAGE_PACK.gettext(v)
        else:
            v = str(v)
        file.write(v)
    file.write(end)

    if flush:
        file.flush()


_input=input
def input(_prompt:object = "") -> str:
    """An emulated version of the default `input`.
    Allows `localizer` to intercept the `_prompt` and provide
    an easy way to translate it to different languages.

    Args:
        _prompt (object, optional): Any object that implements `repr` or `str`. Defaults to "".

    Returns:
        str: A string that's typed to the console (the string is read by the default input function).
    """
    if isinstance(_prompt, str):
        _prompt = GLOBAL_LANGUAGE_PACK.gettext(_prompt)
    return _input(_prompt)
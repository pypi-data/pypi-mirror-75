import ast
import inspect
import pprint
import re

from .bprint import bprint
from colors import *


def dprint(variable, description_func=lambda text: pprint.pformat(text, indent=2)):
    frame = inspect.currentframe()
    frame = inspect.getouterframes(frame)
    frame = frame[1]
    m = re.search("dprint\((.+)\)", frame.code_context[0])
    # TODO: pretty hacky - we need to properly parse the param list and handle
    # edge cases (inlined functions)
    variables = m.group(1).split(",")

    text = f"""
{frame.filename}:{frame.lineno}

type = {type(variable)}
value = {description_func(variable)}
    """

    bprint(
        text,
        title=variables[0],
        stroke_func=lambda text: color(text, fg="yellow"))

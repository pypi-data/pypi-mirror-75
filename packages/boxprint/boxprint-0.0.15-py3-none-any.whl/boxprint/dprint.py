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

    title = ""
    if frame is not None and frame.code_context is not None:
        m = re.search("dprint\((.+)\)", frame.code_context[0])
        # TODO: pretty hacky - we need to properly parse the param list and handle
        # edge cases (inlined functions)
        variables = m.group(1).split(",")
        title = variables[0]

    text = f"""
{frame.filename}:{frame.lineno}

type = {type(variable)}
value = {description_func(variable)}
    """

    bprint(
        text,
        title=title,
        stroke_func=lambda text: color(text, fg="yellow"))

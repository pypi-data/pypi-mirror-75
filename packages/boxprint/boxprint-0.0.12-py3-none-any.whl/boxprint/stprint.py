import sys

from collections import OrderedDict as OD
from .bprint import bprint
from colors import *


def stprint(width=80):
    frame = sys._getframe(1)
    description = []
    description.append("\n")
    for local, value in OD(frame.f_locals).items():
        description.append(f"  {str(local)} = {str(value)}")
        description.append("\n")
    description = "".join(description)
    bprint(
        description,
        title=f"{frame.f_code.co_name} - {frame.f_code.co_filename}:{frame.f_lineno}",
        stroke_func=lambda text: color(text, fg="red"),
        width=width)

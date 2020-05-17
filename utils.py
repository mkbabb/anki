import os
import subprocess
import sys
from typing import *
import json
import re


RE_WHITESPACE = re.compile("\s+")

def file_components(filepath: str) -> Tuple[str, str, str]:
    dirpath = os.path.dirname(os.path.realpath(filepath))
    filename, ext = os.path.splitext(os.path.basename(filepath))
    return (dirpath, filename, ext)


def sanitize_string(s: str, white_space: str = "") -> str:
    if (white_space != ""):
        s = re.sub(RE_WHITESPACE, white_space)
    return s.lower().strip()


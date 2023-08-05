# -*- coding: utf-8 -*-
from pathlib import Path

from .client import Client

__version__ = (Path(__file__).parent / "VERSION").read_text().strip()

from dotenv import load_dotenv
from enum import Enum
from os import environ
load_dotenv()

class TimeScale(Enum):
    CONNECTION=environ["TIMESCALE_URL"]

class Path(Enum):
    LOG_PATH=environ["LOG_PATH"]

class Logo(Enum):
    CMDLOGO="""
            ▀▀█▀▀ ─▀─ █▀▄▀█ █▀▀ ░█▀▀▀█ █▀▀ █▀▀█ █── █▀▀   ░█─░█ █▀▀▄ █▀▀▄ █── █▀▀█ █▀▀ █─█ █▀▀ █▀▀█ 
            ─░█── ▀█▀ █─▀─█ █▀▀ ─▀▀▀▄▄ █── █▄▄█ █── █▀▀   ░█─░█ █──█ █▀▀▄ █── █──█ █── █▀▄ █▀▀ █▄▄▀ 
            ─░█── ▀▀▀ ▀───▀ ▀▀▀ ░█▄▄▄█ ▀▀▀ ▀──▀ ▀▀▀ ▀▀▀   ─▀▄▄▀ ▀──▀ ▀▀▀─ ▀▀▀ ▀▀▀▀ ▀▀▀ ▀─▀ ▀▀▀ ▀─▀▀
            """

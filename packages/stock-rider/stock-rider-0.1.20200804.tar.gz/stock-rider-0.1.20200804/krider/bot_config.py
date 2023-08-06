import configparser
import os

from krider.utils import str_to_bool

DEV_MODE = str_to_bool(os.getenv("IS_DEV"))


def config(key, default_value=None):
    c = configparser.ConfigParser()
    c.read("env.cfg")

    if DEV_MODE:
        return c.get("DEV", key) or default_value
    else:
        return c.get("LIVE", key) or default_value

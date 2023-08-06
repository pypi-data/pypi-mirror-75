from pathlib import Path

from starlette.config import Config

from spell.serving.exceptions import InvalidServerConfiguration


def path_cast(value):
    path = Path(value)
    if not path.exists():
        raise InvalidServerConfiguration(f"Path {value} does not exist")
    return path


config = Config("/config/.env")

# Path to the config file"
CONFIG_FILE = config("CONFIG_FILE", cast=path_cast)
# Path to the Python module containing predictor"
MODULE_PATH = config("MODULE_PATH", cast=path_cast)
# Python path to the module containing the predictor"
PYTHON_PATH = config("PYTHON_PATH")
# Name of the predictor class"
CLASSNAME = config("CLASSNAME", default=None)
# Run the server in debug mode"
DEBUG = config("DEBUG", cast=bool, default=False)

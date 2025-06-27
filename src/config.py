# src/config.py

import os
from dotenv import load_dotenv

load_dotenv()

def get_env_variable(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise EnvironmentError(f"Missing required environment variable: {name}")
    return value

BASE_URL = get_env_variable("BASE_URL")
DATA_DIR = get_env_variable("DATA_DIR")
EXPORT_FILENAME_PREFIX = get_env_variable("EXPORT_FILENAME_PREFIX")

"""Configuration manager for tasks3."""

from .config import load_config

(CONFIG_FILE_PATH, DATA_FOLDER_PATH, DB_BACKEND, DB_PATH,) = load_config()

__all__ = {
    "CONFIG_FILE_PATH",
    "DATA_FOLDER_PATH",
    "DB_BACKEND",
    "DB_PATH",
}

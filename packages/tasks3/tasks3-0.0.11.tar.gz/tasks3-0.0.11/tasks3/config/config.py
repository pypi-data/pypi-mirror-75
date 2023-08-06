import click

from typing import Tuple

from pathlib import Path
from ruamel.yaml import YAML

__root_package__ = __package__.split(".")[0]

DEFAULT_CONFIG_FILE_PATH: Path = Path(click.get_app_dir(__root_package__)).joinpath(
    "config.yml"
)
DEFAULT_DATA_FOLDER_PATH: Path = Path(click.get_app_dir(__root_package__))

SUPPORTED_DB_BACKEND = {
    "mysql",
    "postgresql",
    "sqlite",
}


def load_config(
    config_file_path: Path = DEFAULT_CONFIG_FILE_PATH,
) -> Tuple[Path, Path, str, Path]:
    """Load configuration settings from a config file (yaml)

    :config_file_path: pathlib.Path object to the config file.
    :returns: CONFIG_FILE_PATH, DATA_FOLDER_PATH, DB_BACKEND, DB_PATH
    """
    try:
        config_data = YAML().load(config_file_path)
    except (AttributeError, FileNotFoundError) as e:
        config_data = None
        click.echo(f"Failed to load config file!\n{e}", err=True)
    finally:
        if config_data is None:
            config_data = dict()
    data_folder_path = config_data.get("data folder", DEFAULT_DATA_FOLDER_PATH)

    """Get configuration of the database.

    + DB backend
    + DB path
    """
    db_config: dict = config_data.get("db", dict())
    # Note: If we drop support for python<=3.8
    # switch to using walrus operator here.
    db_backend: str = db_config.get("backend", "sqlite").lower()
    if db_backend not in SUPPORTED_DB_BACKEND:
        raise ValueError(
            f"Only values from {SUPPORTED_DB_BACKEND} are supported. "
            f"{db_backend} was supplied instead."
        )
    db_path: Path = data_folder_path.joinpath(db_config.get("path", "tasks.db"))
    return (config_file_path, data_folder_path, db_backend, db_path)

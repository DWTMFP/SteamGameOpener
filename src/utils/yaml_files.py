import logging
from pathlib import Path

import yaml
from pydantic import ValidationError

from .configs import Config, UserData
from .constants import (
    CONFIG_PYDANTIC_FROM_YAML,
    STANDARD_CONFIG_PATH,
    USER_DATA_PATH,
    USER_DATA_PYDANTIC_FROM_YAML,
    DefaultSteamPath_str,
    UserDataYAMLStrings,
    generate_config_str,
    generate_user_data_str,
)

# ==========================
# == Config and User Data ==
# ==========================

logger = logging.getLogger()


def convert_yaml_keys(data: dict, key_mapping: dict[str, str]) -> dict:
    for key in list(data.keys()):
        value = data.pop(key)

        new_key = key_mapping.get(key)
        if new_key is None:
            logger.warning(f'Unkown key: "{key}", will be skipped')
            continue

        if isinstance(value, dict):
            value = convert_yaml_keys(value, key_mapping)

        data[new_key] = value

    return data


def get_config(config_path: Path) -> Config:
    create_config()
    logger.info("Loading config.")

    if not config_path.exists():
        logger.info(
            f"Config Path doesn't exist. Using default values.\nConfig Path: {config_path}"
        )
        if config_path == STANDARD_CONFIG_PATH:
            create_config()
        return Config()

    try:
        with Path(config_path).open(encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        logger.warning("Invalid YAML syntax: %s", e)
        logger.info("Using default values.")
        return Config()

    if data is None:
        logger.warning("Empty config, please restore or delete it.")
        logger.info("Using default values.")
        return Config()

    try:
        return Config(**convert_yaml_keys(data, CONFIG_PYDANTIC_FROM_YAML))
    except ValidationError as e:
        logger.warning("Invalid config: %s", e)
        logger.info("Using default values.")
        return Config()


def create_config():
    if not STANDARD_CONFIG_PATH.exists():
        logger.info("Creating new config file.")
        STANDARD_CONFIG_PATH.write_text(generate_config_str(), encoding="utf-8")


def get_user_data() -> UserData:
    create_user_data()
    logger.info("Loading user data.")
    try:
        with Path(USER_DATA_PATH).open(encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        logger.warning("Invalid YAML syntax: %s", e)
        logger.info("Using default values.")
        return UserData()

    if data is None:
        logger.warning("Empty userData file, please restore or delete it.")
        logger.info("Using default values.")
        return UserData()

    steam_path = Path(data[UserDataYAMLStrings.steam_path])
    if not steam_path.exists():
        logger.warning(f"Invalid Steam Path, now using {DefaultSteamPath_str}")
        steam_path = Path(DefaultSteamPath_str)

    if not steam_path.exists():
        raise FileNotFoundError("Path to Steam was not found.")

    try:
        user_data = UserData(**convert_yaml_keys(data, USER_DATA_PYDANTIC_FROM_YAML))
    except ValidationError as e:
        logger.warning("Invalid config: %s", e)
        logger.info("Using default values.")
        return UserData()

    return user_data


def create_user_data():
    if not USER_DATA_PATH.exists():
        logger.info("No User Data file found. Creating new one.")
        USER_DATA_PATH.write_text(generate_user_data_str(), encoding="utf8")

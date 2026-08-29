from pydantic import ValidationError
from pathlib import Path
import logging
import yaml
from .constants import (
    STANDARD_CONFIG_PATH, USER_DATA_PATH, CONFIG_PYDANTIC_FROM_YAML, 
    generate_config_str, generate_userData_str,
    DefaultSteamPath_str, USER_DATA_YAML_STRINGS, USER_DATA_PYDANTIC_FROM_YAML
)

from .configs import Config, UserData
# ==========================
# == Config and User Data ==
# ==========================

    
def convert_yaml_keys(data: dict, key_mapping:dict[str,str]) -> dict:
    for key in list(data.keys()):
            value = data.pop(key)

            new_key = key_mapping.get(key)
            if new_key is None:
                logging.warning(f'unkown key: "{key}", will be skipped')
                continue

            if isinstance(value, dict):
                value = convert_yaml_keys(value, key_mapping)
            

            data[new_key] = value

    return data


def get_config(config_path:Path) -> Config:
    create_config()
    logging.info("Loading config.")
    
    if not config_path.exists():
        logging.info(f"Config Path doesn't exist. Using default values.\nConfig Path: {config_path}")
        if config_path == STANDARD_CONFIG_PATH:
            create_config()
        return Config()
    
    try:
        with open(STANDARD_CONFIG_PATH, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        logging.warning("Invalid YAML syntax: %s", e)
        logging.info("Using default values.")
        return Config()
        
    if data is None:
        logging.warning("Empty config, please restore or delete it.")
        logging.info("Using default values.")
        return Config()
    
    try:
        return Config(**convert_yaml_keys(data, CONFIG_PYDANTIC_FROM_YAML))
    except ValidationError as e:
        logging.warning("Invalid config: %s", e)
        logging.info("Using default values.")
        return Config()


def create_config():
    if not STANDARD_CONFIG_PATH.exists():
        logging.info("Creating new config file.")
        STANDARD_CONFIG_PATH.write_text(generate_config_str(), encoding="utf-8")

    
def get_user_data() -> UserData:
    create_user_data()
    logging.info("Loading user data.")
    try:
        with open(USER_DATA_PATH, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        logging.warning("Invalid YAML syntax: %s", e)
        logging.info("Using default values.")
        return UserData()
    
    if data is None:
        logging.warning("Empty userData file, please restore or delete it.")
        logging.info("Using default values.")
        return UserData()
    
    
    steam_path = Path(data[USER_DATA_YAML_STRINGS.steam_path])
    if not steam_path.exists():
        logging.warning(f"Invalid Steam Path, now using {DefaultSteamPath_str}")
        steam_path = Path(DefaultSteamPath_str)

    if not steam_path.exists():
        raise FileNotFoundError("Path to Steam was not found.")
    
    try:
        userData = UserData(**convert_yaml_keys(data, USER_DATA_PYDANTIC_FROM_YAML))
    except ValidationError as e:
        logging.warning("Invalid config: %s", e)
        logging.info("Using default values.")
        return UserData()
    
    return userData


def create_user_data():
    if not USER_DATA_PATH.exists():
        logging.info("No User Data file found. Creating new one.")
        USER_DATA_PATH.write_text(generate_userData_str(), encoding="utf8")
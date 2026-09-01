from app import display_gui, display_game_appid
from utils import (
    STANDARD_CONFIG_PATH, SRC_DIR,
    get_images, get_user_data,
)
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--appids", action="store_true", help = "Show the App ID for every game")
    parser.add_argument("--copy_icons",  action="store_true", help = "Copy the Steam Icons to the image folder")
    parser.add_argument("--no_main",  action="store_true", help = "Does not open the main programm, if this is parsed\tUseful for --copy_icons")
    parser.add_argument("--config", "-c", default=STANDARD_CONFIG_PATH, help = "The Name of the config file")

    args = parser.parse_args()

    
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = SRC_DIR / config_path
    
    if args.copy_icons:
        user_data = get_user_data()
        get_images(user_data)

    if args.appids:
        display_game_appid(config_path)
    elif not args.no_main:
        display_gui(config_path)

if __name__ == "__main__":
    main()
import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path

import requests
from PIL import Image
from PySide6.QtGui import QIcon

from steam_appinfo_parser.parse_appinfo import iter_apps

from .configs import ScrollbarColor, SteamGame, UserData
from .constants import GAMES_PATH, IMG_DIR, USER_DATA_PATH

logger = logging.getLogger()
# ===================
# == Get game data ==
# ===================


@dataclass(frozen=True)
class Game:
    appid: int
    name: str
    install_dir: str
    exe_path: str | None = None


class SteamGameManager:
    def __init__(self, user_data: UserData):
        game_by_appid: dict[int, Game] = {}
        game_by_name: dict[str, Game] = {}

        steam_games = user_data.steam_games

        # Get games from appmanifest files
        for file in Path(user_data.steam_path, "steamapps").glob("appmanifest_*.acf"):
            # Get Appid
            try:
                appid = int(file.stem.removeprefix("appmanifest_"))
            except ValueError:
                msg = f'Tried to convert "{file.stem.removeprefix("appmanifest_")}" to an integer. Failed.'
                logger.exception(msg)
                continue

            # Get Games from appmanifest files
            with file.open(encoding="utf8") as f:
                file_data = f.read().replace('"', "").replace("\t", "").split("\n")

            game = self.__build_game_from_appmanifest(appid, file_data, steam_games)
            game_by_appid[appid] = game
            game_by_name[game.name] = game

        # Get games from user data file
        if user_data.custom_games:
            for custom_game in user_data.custom_games:
                appid = custom_game.appid
                game_name = custom_game.name

                game = Game(
                    name=game_name,
                    appid=appid,
                    install_dir="",
                    exe_path=custom_game.exe_path,
                )

                game_by_appid[appid] = game
                game_by_name[game_name] = game

        self.__game_by_appid = game_by_appid
        self.__game_by_name = game_by_name

        self.__discovered_game_names: list[str] = list(game_by_name.keys())

        self.user_data = user_data
        self.__update_listed_games()

        self.__check_conflicting_name_and_appid(steam_games)

    def __check_conflicting_name_and_appid(self, steam_games: list[SteamGame] | None):
        if not steam_games:
            return

        for steam_game in steam_games:
            if not (steam_game.appid and steam_game.name):
                continue
            # Check if A) AppID exists and B) if the gotten name and the actual name are matching
            try:
                real_name = self.get_game_name(steam_game.appid)
                if steam_game.name != real_name:
                    logger.warning(
                        f"The name and AppID under user data / Steam Games "
                        f"don't match for the following entry: "
                        f'Name: "{steam_game.name}" AppID: "{steam_game.appid}"'
                    )
            except KeyError:
                logger.warning(
                    f"AppID {steam_game.appid} not found. Please check, if it was correct under user data / Steam Games."
                )

            # check if A) name exists and B) if the gotten AppId and the actual AppId are matching
            try:
                real_appid = self.get_appid(steam_game.name)
                if real_appid != steam_game.appid:
                    logger.warning(
                        f"The name and AppID under user data / Steam Games "
                        f"don't match for the following entry: "
                        f'Name: "{steam_game.name}" AppID: "{steam_game.appid}"'
                    )
            except KeyError:
                logger.warning(
                    f"Steam Game {steam_game.name} not found. Please check, if it was correct under user data / Steam Games."
                )

    def __build_game_from_appmanifest(
        self, appid: int, file_data: list[str], steam_games: list[SteamGame] | None
    ) -> Game:
        # get game_name and install_dir
        game_name = ""
        install_dir = ""
        for line in file_data:
            if line.startswith("name"):
                game_name = line.removeprefix("name")

            elif line.startswith("installdir"):
                install_dir = line.removeprefix("installdir")

            if game_name and install_dir:
                break

        return Game(
            appid,
            game_name,
            install_dir,
            self.__get_exe_path(appid, game_name, steam_games),
        )

    def __get_exe_path(
        self, appid: int, game_name: str, steam_games: list[SteamGame] | None
    ) -> str | None:
        # == Actual Function start ==
        if steam_games is None:
            return None

        # First try to find by AppID
        for steam_game in steam_games:
            if steam_game.appid == appid:
                return steam_game.exe_path

        # Matching name as Fallback
        for steam_game in steam_games:
            if steam_game.name == game_name:
                return steam_game.exe_path
        return None

    def __update_listed_games(self):
        """Does NOT edit the txt file, it reads it again, to get new games to display"""
        game_names = self.__get_games_from_txt()
        games: list[Game] = []

        for game_name in game_names:
            if game_name not in self.__game_by_name:
                logger.warning(f"Game {game_name} appears to be deinstalled.")
                continue
            appid = self.get_appid(game_name)
            install_dir = self.get_install_dir(game_name=game_name)
            games.append(Game(appid, game_name, install_dir))
        self.__listed_games = games

    def get_listed_games(self) -> list[Game]:
        return self.__listed_games

    def get_appid(self, game_name: str) -> int:
        return self.__game_by_name[game_name].appid

    def get_game_name(self, appid: int) -> str:
        return self.__game_by_appid[appid].name

    def get_game(
        self, *, appid: int | None = None, game_name: str | None = None
    ) -> Game:
        r"""
        One of these parameters has to be parsed as a keyword argument. Additionally if both are given, ``appid`` takes priority\n

        :param int | None = None appid: The AppID of the game you want the install dir of
        :param str | None = None game_name: The game name of the game you want the install dir of
        :returns Game: Game object of of given game
        """
        if appid is None and game_name is None:
            raise ValueError("Either 'appid' or 'game_name' must be provided.")

        if appid is not None:
            return self.__game_by_appid[appid]

        return self.__game_by_name[game_name]  # pyright: ignore[reportArgumentType]

    def get_all_games(self):
        return list(self.__game_by_name.values())

    def get_install_dir(
        self, *, appid: int | None = None, game_name: str | None = None
    ) -> str:
        r"""
        One of these parameters has to be parsed as a keyword argument. Additionally if both are given, ``appid`` takes priority\n

        :param int | None = None appid: The AppID of the game you want the install dir of
        :param str | None = None game_name: The game name of the game you want the install dir of
        :returns str: Install directory of given game
        """
        return self.get_game(appid=appid, game_name=game_name).install_dir

    def __get_games_from_txt(self) -> list[str]:
        if not GAMES_PATH.exists():
            return []
        with Path(GAMES_PATH).open(encoding="utf8") as f:
            text = f.read()

        # set it here to preserve empty lines and comments starting with a "#"
        self.__original_text_file = text

        text = text.split("\n")

        games = []
        for line in text:
            stripped_line = line.strip()
            # Skip line, if empty or starts with a "#" (comment)
            if not stripped_line or stripped_line.startswith("#"):
                continue
            games.append(line)
        return games

    def write_games_to_txt(self):
        logger.info("Writing new games into txt file.")
        s = ""
        # split old and new games to not change the order of old games and add the new ones on the bottom
        all_games: list[str] = self.__discovered_game_names
        current_games: list[str] = [game.name for game in self.__listed_games]

        games_to_add = [
            game for game in all_games if game not in current_games
        ]  # [games] - [old_games]

        if games_to_add == []:
            logger.info("No new games found, not overwriting text file.")
            return

        s = self.__original_text_file
        s += "\n"
        s += "\n".join(games_to_add)
        s = s.strip()  # no trailing newline

        with Path(GAMES_PATH).open("w", encoding="utf8") as file:
            file.write(s)

        self.__update_listed_games()
        logger.info("Done.")


def _download_image(url: str, name: str):
    """
    Download the image given by the url.

    :param str url: The url to the image
    :param str name: The name of the new file, without extension
    """
    response = requests.get(url, timeout=10)

    if response.status_code == requests.status_codes.codes.ok:
        if not IMG_DIR.exists():
            IMG_DIR.mkdir()

        img_file = name + ".jpg"
        with Path(IMG_DIR, img_file).open("wb") as fp:
            fp.write(response.content)
    else:
        print(response.status_code)


def download_images(user_data: UserData):
    logger.info("Trying to download Images.")
    used_appids = [file.stem for file in [*IMG_DIR.glob("*.jpg")]]
    steam_path = Path(user_data.steam_path)

    if not steam_path.exists():
        logger.warning(f"Steam Path {str(steam_path)} doesn't exist.")
        return

    # in Steam/steamapps there are appmanifest_{appid}.acf files, file.stem removes the rest of the path along with the extension
    all_appids = [
        int(file.stem.removeprefix("appmanifest_"))
        for file in Path(steam_path, "steamapps").glob("appmanifest_*")
    ]
    appids_to_download = [appid for appid in all_appids if appid not in used_appids]
    if appids_to_download == []:
        logger.info("No new games found, skipping request.")
        return

    print(appids_to_download)

    game_icons = {}

    api_url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={user_data.api_key}&steamid={user_data.profile_id}&format=json&include_played_free_games=1&include_appinfo=1&skip_unvetted_apps=false&include_free_sub"
    response = requests.get(api_url, timeout=10)

    if response.status_code != requests.status_codes.codes.ok:
        logger.warning(f"Something went wrong. Status Code: {response.status_code}")
        return
    response = response.json()["response"]

    if "games" not in response:
        logger.warning("Couldn't download images. API response didn't include games")
        return

    for game in response["games"]:
        game_icons[str(game["appid"])] = game["img_icon_url"]
        print(game)

    for appid in appids_to_download:
        if (
            appid in game_icons
        ):  # don't try to download games, which the api, didn't return
            img = f"http://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{game_icons[appid]}.jpg"
            _download_image(img, str(appid))
            logger.info(f"Downloaded image {str(appid) + '.jpg'}")


def run_exe(path: Path):
    logger.info(f"Running {str(path)}")
    os.startfile(path)
    sys.exit()


def get_QScrollBar_style_sheet(color: ScrollbarColor) -> str:  # noqa: N802
    return f"""
    QScrollBar:vertical {{
        background: {color.background};
        width: 16px;
        border: 1px {color.border};
    }}

    QScrollBar::handle:vertical {{
        background: {color.handle};
        border: 1px {color.border};
        min-height: 20px;
    }}

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {{
        background: gray;
        height: 0px;
        border: 1px {color.border};
    }}

    QScrollBar::add-page:vertical,
    QScrollBar::sub-page:vertical {{
        background: {color.background};
    }}

        QScrollBar:horizontal {{
    background: {color.background};
    height: 16px;
    border: 1px {color.border};
}}

QScrollBar::handle:horizontal {{
    background: {color.handle};
    border: 1px {color.border};
    min-width: 20px;
}}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {{
    background: gray;
    width: 0px;
    border: 1px {color.border};
}}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {{
    background: {color.background};
}}
"""


def _get_appid_by_hash(path: Path) -> dict[str, int] | None:
    """
    Get a dictionary for looking up the appid, with the hash as an input

    :param Path path: The path to the appinfo.vdf file
    :returns dict[str, int] | None: Returns ``None`` if the appinfo.vdf file is not existent, otherwise return the dictionary for appid lookup.
    """
    if not path.exists():
        return None

    data = path.read_bytes()
    appid_by_hash = {}

    for game in iter_apps(data):
        common = game.get("common", {})
        clienticon = common.get("clienticon")

        if game.get("type") == "game" and game.get("appid") is not None and clienticon:
            appid_by_hash[clienticon] = game["appid"]

    return appid_by_hash


def _get_existing_hashes(steam_img_dir: Path) -> list[str]:
    return [file.stem for file in steam_img_dir.glob("*.ico")]


def _copy_icon_to_image_folder(icon_hash: str, appid: int | None, steam_icon_dir: Path):
    new_name = str(appid) if appid is not None else icon_hash

    source_path = steam_icon_dir / (icon_hash + ".ico")

    if not source_path.exists():
        logger.warning(f"Icon not found: {source_path}")
        return

    destination_path = IMG_DIR / (new_name + ".jpeg")
    # For also supporting .png files
    for img_format in (".jpg", ".png"):
        if destination_path.with_suffix(img_format).exists():
            return

    with Image.open(source_path) as image:
        image.convert("RGB").save(destination_path, "JPEG")


def copy_icons(user_data: UserData):
    r"""
    Copy the Icons offline

    Copys the .ico files from Steam/steam/games to src/images\n
    Unfortunately, the names are hashes, not appids, so auto convertion is only sometimes possible
    """
    steam_path = Path(user_data.steam_path)
    if not steam_path.exists():
        logger.warning(f"Steam Path {str(steam_path)} doesn't exist.")
        return

    appinfo_path = steam_path / "appcache" / "appinfo.vdf"
    appid_by_hash = _get_appid_by_hash(appinfo_path)
    if appid_by_hash is None:
        logger.warning(
            "The Path to ``appinfo.vdf`` does not exist. Please open Steam to create that file."
        )
        return
    steam_icon_dir = steam_path / "steam" / "games"
    not_identified_icons = set()

    existing_hashes = _get_existing_hashes(steam_icon_dir)

    # hashes to ignore can be None, validate_list doesn't acceppt None, but might return it
    hashes_to_ignore = user_data.get_game_icons.hashes_to_ignore

    # Try identifying via appinfo.vdf
    for icon_hash in existing_hashes:
        if icon_hash in hashes_to_ignore:
            continue
        if icon_hash not in appid_by_hash:
            not_identified_icons.add(icon_hash)
            _copy_icon_to_image_folder(icon_hash, None, steam_icon_dir)
        else:
            _copy_icon_to_image_folder(
                icon_hash, appid_by_hash[icon_hash], steam_icon_dir
            )

    # == NO WORKING CASE FOUND ==
    # == UNFORTUNATLY HASHES APPEAR TO BE DIFFERENT AND SOMETIMES DIFFERENT IMAGES ==
    # Try identifying via libraryfolder
    # librarycache_folder = steam_path / "appcache" / "librarycache"
    # steam_manager = SteamGameManager(user_data)

    # for game in steam_manager.get_all_games():
    #     appid = str(game.appid)

    #     appid_name = IMG_DIR / f"{appid}.jpg"
    #     if appid_name.exists():
    #         continue

    #     game_path = librarycache_folder / appid

    #     if not game_path.exists():
    #         logging.debug(f"Didn't find folder: {game_path}")
    #         continue

    #     for jpg in game_path.glob("*.jpg"):
    #         icon_hash = jpg.stem

    #         # Hash either already identified, or wrong image
    #         if icon_hash not in not_identified_icons:
    #             continue

    #         hash_name = IMG_DIR / f"{icon_hash}.jpg"

    #         hash_name.rename(appid_name)
    #         not_identified_icons.discard(icon_hash)
    #         break

    ignore_unokwn_hashes = user_data.get_game_icons.ignore_unkown_hashes

    if ignore_unokwn_hashes:
        for icon_hash in not_identified_icons:
            img_path = IMG_DIR / f"{icon_hash}.jpg"
            img_path.unlink(missing_ok=True)

    if not_identified_icons:
        # DO NOT REMOVE THE SPACES, THEY ALIGN THE NEWLINES WITH THE TEXT AFTER "Warning: "
        logging_str = (
            f"Could not automatically identify {len(not_identified_icons)} icons.\n         "
            f'Please add them manually and add them to the "Hashes to Ignore" list in {USER_DATA_PATH}:\n         '
            + "\n         ".join(not_identified_icons)
            + "\n         To get the corresponding AppID run: py main.py --appid"
        )
        logger.warning(logging_str)


def get_images(user_data: UserData):
    """Fetch the images with the specified method"""
    source = user_data.get_game_icons.source
    # Create IMG_DIR if it doesn't exist yet
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    if source == "online":
        if user_data.profile_id and user_data.api_key:
            download_images(user_data)
        else:
            logger.warning(
                "Both Profile ID and API Key must be provided for online checking.\n         "
                'Consider using "auto" as your image source'
            )
    elif source == "offline":
        copy_icons(user_data)
    elif source == "auto":
        if user_data.profile_id and user_data.api_key:
            download_images(user_data)
        else:
            copy_icons(user_data)


def get_icon_from_appid(appid: int) -> QIcon | None:
    for img_format in (".png", ".jpg", ".jpeg"):
        img_name = str(appid) + img_format
        img_path = IMG_DIR / img_name
        if img_path.exists():
            return QIcon(str(img_path))
    return None

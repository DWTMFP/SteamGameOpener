from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import Field

# Paths and directories
SRC_DIR = (
    Path(__file__).resolve().parent.parent
)  # Path(__file__) → src/utils/constants.py
STANDARD_CONFIG_PATH = SRC_DIR / "config.yaml"
USER_DATA_PATH = SRC_DIR / "userData.yaml"
IMG_DIR = SRC_DIR / "Images"
GAMES_PATH = SRC_DIR / "games.txt"

DefaultSteamPath_str = r"C:\Program Files (x86)\Steam"


def _to_yaml_value(
    value: bool | str | int | Iterable | None,  # noqa: FBT001
    *,
    indent: int | None = None,
) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, str):
        return f'"{value}"'
    if isinstance(value, Iterable):
        s = "\n"
        if indent:
            s += indent * " "
        s += "-"
        for item in value:
            s += " " + _to_yaml_value(item) + "\n"
            if indent:
                s += indent * " "
            s += "-"
        return s

    return str(value)


@dataclass(frozen=True)
class YAMLValue:
    yaml_key: str
    default: Any = None
    default_factory: Callable[[], Any] | None = None

    def get_default(self) -> Any:
        if self.default_factory is not None:
            return self.default_factory()

        return self.default

    def yaml_default(self, *, indent: int | None = None) -> str:
        return _to_yaml_value(self.get_default(), indent=indent)

    def to_yaml_line(
        self,
        space_after_colon: int = 1,
        space_before_default: int = 1,
        with_default: bool = True,  # noqa: FBT001, FBT002
        *,
        indent: int | None = None,
    ):
        value = self.yaml_default(indent=indent)
        separator_after_colon = " " * space_after_colon
        default_separator = " " * space_before_default

        line = f"{self.yaml_key}:{separator_after_colon}{value}"

        if with_default:
            line += f"{default_separator}#default: {value}"

        return line

    def pydantic_field(self):
        if self.default_factory is not None:
            return Field(
                default_factory=self.default_factory,
                alias=self.yaml_key,
            )
        if self.default is not None:
            return Field(
                default=self.default,
                alias=self.yaml_key,
            )
        return Field(alias=self.yaml_key)


class ConfigValues:
    # Main Window
    main_window = YAMLValue("Main Window")
    window_title = YAMLValue(yaml_key="Title", default="Steam Games")
    window_background = YAMLValue(yaml_key="Background", default="black")
    window_foreground = YAMLValue(yaml_key="Foreground", default="white")

    window_position = YAMLValue("Position")
    window_x_pos = YAMLValue(yaml_key="x", default=None)
    window_y_pos = YAMLValue(yaml_key="y", default=None)

    window_size = YAMLValue("Size")
    window_width = YAMLValue(yaml_key="Width", default=None)
    window_height = YAMLValue(yaml_key="Height", default=None)

    window_font = YAMLValue("Font")
    font_family = YAMLValue(yaml_key="Family", default="Arial")
    font_size = YAMLValue(yaml_key="Size", default=20)

    window_img_size = YAMLValue(yaml_key="Image size", default=31)

    # Scrollbar
    scrollbar = YAMLValue("Scrollbar")
    scrollbar_off = YAMLValue(yaml_key="Deactivate Scrollbar", default=False)
    scrollbar_custom = YAMLValue(yaml_key="Custom Scrollbar", default=False)

    scrollbar_color = YAMLValue("Color")
    scrollbar_color_background = YAMLValue(yaml_key="Background", default="lightgrey")
    scrollbar_color_handle = YAMLValue(yaml_key="Handle", default="grey")
    scrollbar_color_border = YAMLValue(yaml_key="Border", default="solid black")

    # Sorting
    sort_by = YAMLValue("Sort By")
    sort_by_appid = YAMLValue(yaml_key="Appid", default=False)
    sort_by_custom = YAMLValue(yaml_key="Custom Order", default=True)

    # Games
    games = YAMLValue("Games")
    games_exclude = YAMLValue(yaml_key="Exclude", default_factory=list)
    games_show_only = YAMLValue(yaml_key="Only show", default_factory=list)
    games_hide_steamworks = YAMLValue(
        yaml_key="Hide SteamworksCommon Redistributable", default=True
    )


class UserDataValues:
    steam_path = YAMLValue(
        yaml_key="Steam Path", default=DefaultSteamPath_str.replace("\\", "\\\\")
    )
    api_key = YAMLValue(yaml_key="Steam API Key", default="")
    profile_id = YAMLValue(yaml_key="Steam Profile ID", default="")

    steam_games = YAMLValue(yaml_key="Steam Games", default_factory=list)
    steam_games_name = YAMLValue("Name", default=None)
    steam_games_appid = YAMLValue("AppID", default=None)
    steam_games_exe_path = YAMLValue("Exe Path")

    custom_games = YAMLValue(yaml_key="Custom Games", default_factory=list)
    custom_games_name = YAMLValue("Name")
    custom_games_exe_path = YAMLValue("Exe Path")
    custom_games_appid = YAMLValue("AppID")

    get_game_icons = YAMLValue("Get Game Icons")
    hashes_to_ignore = YAMLValue(yaml_key="Hashes to Ignore", default=("SteamMovie",))
    ignore_unkown_hashes = YAMLValue(yaml_key="Ignore unkown Hashes", default=False)
    source = YAMLValue(yaml_key="Source", default="auto")


def generate_config_str():
    return f"""{ConfigValues.main_window.yaml_key}:
  {ConfigValues.window_title.to_yaml_line()}
  {ConfigValues.window_background.to_yaml_line(space_before_default=2)}
  {ConfigValues.window_foreground.to_yaml_line(space_before_default=2)}

  {ConfigValues.window_position.yaml_key}:
    # If both x and y position are set to "null", the window will be centered
    {ConfigValues.window_x_pos.to_yaml_line()}
    {ConfigValues.window_y_pos.to_yaml_line()}

  {ConfigValues.window_size.yaml_key}:
    # If both width and height are set to "null", the window automatically adjustes it's size
    {ConfigValues.window_width.to_yaml_line(space_after_colon=2)}
    {ConfigValues.window_height.to_yaml_line()}

  {ConfigValues.window_font.yaml_key}:
    {ConfigValues.font_family.to_yaml_line()}
    {ConfigValues.font_size.to_yaml_line(space_after_colon=4, space_before_default=5)}

  {ConfigValues.window_img_size.to_yaml_line()}

{ConfigValues.scrollbar.yaml_key}:
  # Turns off the vertical Scrollbar
  {ConfigValues.scrollbar_off.to_yaml_line()}

  # If False the standard Scrollbar will be used. Otherwise it uses the Scrollbar Config.
  {ConfigValues.scrollbar_custom.to_yaml_line()}

  {ConfigValues.scrollbar_color.yaml_key}:
    {ConfigValues.scrollbar_color_background.to_yaml_line(space_before_default=3)}
    {ConfigValues.scrollbar_color_handle.to_yaml_line(space_after_colon=5, space_before_default=8)}
    {ConfigValues.scrollbar_color_border.to_yaml_line(space_after_colon=5)}, apparently needs "solid" in front of it


{ConfigValues.sort_by.yaml_key}:
  # To change the order of games, go to the games.txt file (will be created, upon first start) and change the order of games there
  # you are allowed to insert lines without characters
  # Additionally deleting one game from there, makes it dissapear (until next rescan (update button))
  # If you want to exclude a game from showing up, {ConfigValues.games_exclude} is recommended, because otherwise they will be readded
  # ``SORT_BY_CUSTOM_ORDER`` takes priorisation over ``SORT_BY_APPID``

  {ConfigValues.sort_by_appid.to_yaml_line(space_after_colon=8)}
  {ConfigValues.sort_by_custom.to_yaml_line(space_before_default=2)}

{ConfigValues.games.yaml_key}:
  # To add games, write their name after the minus (-)
  # Every Game needs a newline with a minus in front
  {ConfigValues.games_exclude.to_yaml_line(with_default=False, indent=4)}
  # only_show overwrites exclude
  {ConfigValues.games_show_only.to_yaml_line(with_default=False, indent=4)}

  {ConfigValues.games_hide_steamworks.to_yaml_line()}
"""


def generate_user_data_str():
    return rf"""# The path to the steam installation is necessary, in order to get your games

# The Steam API Key and the Steam Profile ID are only needed, if you want to have the Icons of the Steam Games in the programm to reliably appear.
# The online fetching of images doesn't work if the games are in your family library.
# To fetch icons offline change "Source" under "Get Game Icons" to "offline"
# Then run: py main.py --copy_icons --no_main or py main.py and click on Update

# You then might be prompted to run py main.py --appids, do that, and rename the unidentified hashes to their corresponding appid


# The Path to the Steam folder
# the given path is the standard path, if installed for all users
# The last character doesn't need to be a backslash \
# Insert the path between the apostrophes
{UserDataValues.steam_path.to_yaml_line()}


# You can only create a API Key, if you have spent money on Steam (afaik 5€)
# Create a Steam-Web-API-Key here
# http://steamcommunity.com/dev/apikey
# ----------------------------------------------
# | NEVER SHARE THIS FILE OR YOUR STEAMAPI KEY |
# ----------------------------------------------
{UserDataValues.api_key.to_yaml_line(with_default=False)}


# To get your profile ID, go into Steam -> Settings
# The link in the upper left corner has the form of https://steamcommunity.com/profiles/<profile ID>/
# If you click on that link, it will copy to clipboard, making it easier for you to enter your ID here
# Again insert it between the apostrophes
{UserDataValues.profile_id.to_yaml_line(with_default=False)}

# Add the relative Exe Path to a game, for which the Exe is not found automatically
# either Name or AppID is required; If both are given, the Appid will override the Name
# Fields:
# Name: The name of the Game (e. g. "Doki Doki Literature Club")
# AppID: The appid of the Game (e. g. 698780)
# Exe Path: The relativ path from Steam/steamapps to the exe (e. g. "Doki Doki Literature Club\\DDLC.exe")
{UserDataValues.steam_games.to_yaml_line(with_default=False, indent=2)}

# Set your custom games by adding one to the list
# Fields:
# Name: The name of your game (e. g. "Trackmania Nations Forever")
# Exe Path: The Path to the games Exe (e. g. "C:\\Program Files (x86)\\TmNationsForever\\TmForever.exe")
# AppID: Your custom AppID; Needs to be negative to not contradict Real Appids; Needed for the Image Identification (e. g. -1)
{UserDataValues.custom_games.to_yaml_line(with_default=False, indent=2)}


{UserDataValues.get_game_icons.yaml_key}:
  # When copying icons from Steam/steam/games, ignore these names.
  # This is useful if a hash cannot be automatically identified, but was manually added.
  {UserDataValues.hashes_to_ignore.to_yaml_line(with_default=False, indent=4)}

  # If True, unknown hashes will not be copied when fetching icons offline.
  {UserDataValues.ignore_unkown_hashes.to_yaml_line()}

  # declares how it fetches the icons:
  # auto:
  #   Try to fetch icons online. If the Steam API Key or Steam Profile ID is missing, fall back to offline fetching.
  # offline:
  #   Only fetch icons using the combination of Steam/steam/games and Steam/appcache/appinfo.vdf
  # online:
  #   Always use the Steam Web API
  {UserDataValues.source.to_yaml_line()}
"""  # noqa: S608

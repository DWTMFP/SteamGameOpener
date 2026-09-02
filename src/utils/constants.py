from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

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
class DefaultConfigValues:
    window_title = "Steam Games"
    window_background = "black"
    window_foreground = "white"
    window_x_pos = None
    window_y_pos = None
    window_widht = None
    window_height = None
    window_font_family = "Arial"
    window_font_size = 20
    window_img_size = 31

    scollbar_handle_color = "grey"
    scollbar_background = "lightgrey"
    scrollbar_border_color = "solid black"

    sort_by_appid = False
    sort_by_custom = True

    excluded_games: list = field(default_factory=list)
    show_only_games: list = field(default_factory=list)
    hide_steamworks_commmon = True


@dataclass(frozen=True)
class ConfigYAMLStrings:
    main_window = "Main Window"
    window_title = "title"
    window_background = "background"
    window_foreground = "foreground"
    window_pos = "Position"
    window_x_pos = "x"
    window_y_pos = "y"
    window_size = "Size"
    window_width = "width"
    window_height = "height"
    window_font = "Font"
    font_family = "family"
    font_size = "size"
    img_size = "Image size"

    scrollbar = "Scrollbar"
    scrollbar_color = "color"
    scrollbar_color_background = "background"
    scrollbar_color_handle = "handle"
    scrollbar_color_border = "border"

    sort_by = "Sort By"
    sort_by_appid = "Appid"
    sort_by_custom = "Custom Order"

    games = "Games"
    games_exlude = "exlude"
    games_show_only = "only show"
    games_hide_steamworks = "Hide SteamworksCommon Redistributable"


CONFIG_PYDANTIC_FROM_YAML = {
    ConfigYAMLStrings.main_window: "main_window",
    ConfigYAMLStrings.window_title: "title",
    ConfigYAMLStrings.window_background: "background",
    ConfigYAMLStrings.window_foreground: "foreground",
    ConfigYAMLStrings.window_pos: "position",
    ConfigYAMLStrings.window_x_pos: "x",
    ConfigYAMLStrings.window_y_pos: "y",
    ConfigYAMLStrings.window_size: "window_size",
    ConfigYAMLStrings.window_width: "width",
    ConfigYAMLStrings.window_height: "height",
    ConfigYAMLStrings.window_font: "font",
    ConfigYAMLStrings.font_family: "family",
    ConfigYAMLStrings.font_size: "font_size",
    ConfigYAMLStrings.img_size: "size_of_images",
    ConfigYAMLStrings.scrollbar: "scrollbar",
    ConfigYAMLStrings.scrollbar_color: "color",
    ConfigYAMLStrings.scrollbar_color_background: "background",
    ConfigYAMLStrings.scrollbar_color_handle: "handle",
    ConfigYAMLStrings.scrollbar_color_border: "border",
    ConfigYAMLStrings.sort_by: "sort_by",
    ConfigYAMLStrings.sort_by_appid: "appid",
    ConfigYAMLStrings.sort_by_custom: "custom",
    ConfigYAMLStrings.games: "games",
    ConfigYAMLStrings.games_exlude: "exclude",
    ConfigYAMLStrings.games_show_only: "only_show",
    ConfigYAMLStrings.games_hide_steamworks: "hide_steamworks_common_redistributables",
}


@dataclass(frozen=True)
class DefaultUserDataValues:
    steam_path = DefaultSteamPath_str.replace("\\", "\\\\")  # double \ is needed
    api_key = ""
    profile_id = ""

    hashes_to_ignore: tuple[str | None] = ("SteamMovies",)
    ignore_unkown_hashes = False
    source = "auto"


@dataclass(frozen=True)
class UserDataYAMLStrings:
    steam_path = "Steam Path"
    api_key = "Steam API Key"
    profile_id = "Steam Profile ID"

    get_game_icons = "Get Game Icons"
    hashes_to_ignore = "Hashes to Ignore"
    ignore_unkown = "Ignore unkown Hashes"
    source = "Source"


USER_DATA_PYDANTIC_FROM_YAML = {
    UserDataYAMLStrings.steam_path: "steam_path",
    UserDataYAMLStrings.api_key: "api_key",
    UserDataYAMLStrings.profile_id: "profile_id",
    UserDataYAMLStrings.get_game_icons: "get_game_icons",
    UserDataYAMLStrings.hashes_to_ignore: "hashes_to_ignore",
    UserDataYAMLStrings.ignore_unkown: "ignore_unkown",
    UserDataYAMLStrings.source: "source",
}


def generate_config_str():
    window_title = _to_yaml_value(DefaultConfigValues.window_title)
    window_background = _to_yaml_value(DefaultConfigValues.window_background)
    window_foreground = _to_yaml_value(DefaultConfigValues.window_foreground)
    window_x_pos = _to_yaml_value(DefaultConfigValues.window_x_pos)
    window_y_pos = _to_yaml_value(DefaultConfigValues.window_y_pos)
    window_widht = _to_yaml_value(DefaultConfigValues.window_widht)
    window_height = _to_yaml_value(DefaultConfigValues.window_height)
    window_font_family = _to_yaml_value(DefaultConfigValues.window_font_family)
    window_font_size = _to_yaml_value(DefaultConfigValues.window_font_size)
    window_img_size = _to_yaml_value(DefaultConfigValues.window_img_size)

    scrollbar_handle_color = _to_yaml_value(DefaultConfigValues.scollbar_handle_color)
    scrollbar_backgound = _to_yaml_value(DefaultConfigValues.scollbar_background)
    scrollbar_border_color = _to_yaml_value(DefaultConfigValues.scrollbar_border_color)

    sort_by_appid = _to_yaml_value(DefaultConfigValues.sort_by_appid)
    sort_by_custom = _to_yaml_value(DefaultConfigValues.sort_by_custom)

    excluded_games = _to_yaml_value(DefaultConfigValues.excluded_games, indent=4)
    show_only_games = _to_yaml_value(DefaultConfigValues.show_only_games, indent=4)
    hide_steamworks_commmon = _to_yaml_value(
        DefaultConfigValues.hide_steamworks_commmon
    )

    default_config = f"""{ConfigYAMLStrings.main_window}:
  {ConfigYAMLStrings.window_title}: {window_title} #default: {window_title}
  {ConfigYAMLStrings.window_background}: {window_background}  #default: {window_background}
  {ConfigYAMLStrings.window_foreground}: {window_foreground}  #default: {window_foreground}

  {ConfigYAMLStrings.window_pos}:
    # If both x and y position are set to "null", the window will be centered
    {ConfigYAMLStrings.window_x_pos}: {window_x_pos} #default: {window_x_pos}
    {ConfigYAMLStrings.window_y_pos}: {window_y_pos} #default: {window_y_pos}

  {ConfigYAMLStrings.window_size}:
    # If both width and height are set to "null", the window automatically adjustes it's size
    {ConfigYAMLStrings.window_width}:  {window_widht} #default: {window_widht}
    {ConfigYAMLStrings.window_height}: {window_height} #default: {window_height}

  {ConfigYAMLStrings.window_font}:
    {ConfigYAMLStrings.font_family}: {window_font_family} #default: {window_font_family}
    {ConfigYAMLStrings.font_size}:   {window_font_size}      #default: {window_font_size}

  {ConfigYAMLStrings.img_size}: {window_img_size} #default: {window_img_size}

{ConfigYAMLStrings.scrollbar}:
  {ConfigYAMLStrings.scrollbar_color}:
    {ConfigYAMLStrings.scrollbar_color_background}: {scrollbar_backgound}   #default: {scrollbar_backgound}
    {ConfigYAMLStrings.scrollbar_color_handle}:     {scrollbar_handle_color}        #default: {scrollbar_handle_color}
    {ConfigYAMLStrings.scrollbar_color_border}:     {scrollbar_border_color} #default: {scrollbar_border_color}, apparently needs "solid" in front of it


{ConfigYAMLStrings.sort_by}:
  # To change the order of games, go to the games.txt file (will be created, upon first start) and change the order of games there
  # you are allowed to insert lines without characters
  # Additionally deleting one game from there, makes it dissapear (until next rescan (update button))
  # If you want to exclude a game from showing up, {ConfigYAMLStrings.games_exlude} is recommended, because otherwise they will be readded
  # ``SORT_BY_CUSTOM_ORDER`` takes priorisation over ``SORT_BY_APPID``

  {ConfigYAMLStrings.sort_by_appid}:  {sort_by_appid} #default: {sort_by_appid}
  {ConfigYAMLStrings.sort_by_custom}: {sort_by_custom}  #default: {sort_by_custom}

{ConfigYAMLStrings.games}:
  # To add games, write their name after the minus (-)
  # Every Game needs a newline with a minus in front
  {ConfigYAMLStrings.games_exlude}: {excluded_games}
  # only_show overwrites exclude
  {ConfigYAMLStrings.games_show_only}: {show_only_games}

  {ConfigYAMLStrings.games_hide_steamworks}: {hide_steamworks_commmon} #default: {hide_steamworks_commmon}
"""
    return default_config


def generate_user_data_str():
    steam_path = _to_yaml_value(DefaultUserDataValues.steam_path)
    api_key = _to_yaml_value(DefaultUserDataValues.api_key)
    profile_id = _to_yaml_value(DefaultUserDataValues.profile_id)
    hashes_to_ignore = _to_yaml_value(DefaultUserDataValues.hashes_to_ignore, indent=4)
    ignore_unkown_hashes = _to_yaml_value(DefaultUserDataValues.ignore_unkown_hashes)
    source = _to_yaml_value(DefaultUserDataValues.source)

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
{UserDataYAMLStrings.steam_path}: {steam_path} #default: {steam_path}



# You can only create a API Key, if you have spent money on Steam (afaik 5€)
# Create a Steam-Web-API-Key here
# http://steamcommunity.com/dev/apikey
# ----------------------------------------------
# | NEVER SHARE THIS FILE OR YOUR STEAMAPI KEY |
# ----------------------------------------------
{UserDataYAMLStrings.api_key}: {api_key}


# To get your profile ID, go into Steam -> Settings
# The link in the upper left corner has the form of https://steamcommunity.com/profiles/<profile ID>/
# If you click on that link, it will copy to clipboard, making it easier for you to enter your ID here
# Again insert it between the apostrophes
{UserDataYAMLStrings.profile_id}: {profile_id}

{UserDataYAMLStrings.get_game_icons}:
  # When copying icons from Steam/steam/games, ignore these names.
  # This is useful if a hash cannot be automatically identified, but was manually added.
  {UserDataYAMLStrings.hashes_to_ignore}: {hashes_to_ignore}

  # If True, unknown hashes will not be copied when fetching icons offline.
  {UserDataYAMLStrings.ignore_unkown}: {ignore_unkown_hashes} #default: {ignore_unkown_hashes}

  # declares how it fetches the icons:
  # auto:
  #   Try to fetch icons online. If the Steam API Key or Steam Profile ID is missing, fall back to offline fetching.
  # offline:
  #   Only fetch icons using the combination of Steam/steam/games and Steam/appcache/appinfo.vdf
  # online:
  #   Always use the Steam Web API
  {UserDataYAMLStrings.source}: {source} # default {source}
"""

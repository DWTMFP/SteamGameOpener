from pydantic import BaseModel, Field
from typing import Literal

from .constants import DefaultConfigValues, DefaultUserDataValues
# == CONFIG ==

class Position(BaseModel):
    x: int | None = DefaultConfigValues.window_x_pos
    y: int | None = DefaultConfigValues.window_y_pos

class Size(BaseModel):
    width: int | None = DefaultConfigValues.window_widht
    height: int | None = DefaultConfigValues.window_height

class Font(BaseModel):
    family: str  = DefaultConfigValues.window_font_family
    size: int = DefaultConfigValues.window_font_size

class MainWindow(BaseModel):
    title: str = DefaultConfigValues.window_title
    background:str = DefaultConfigValues.window_background
    foreground:str = DefaultConfigValues.window_foreground
    
    position: Position = Field(default_factory = Position)
    size: Size = Field(default_factory = Size)
    font: Font = Field(default_factory = Font)
    size_of_images: int | None = DefaultConfigValues.window_img_size

class ScrollbarColor(BaseModel):
    background:str = DefaultConfigValues.scollbar_background
    handle:str = DefaultConfigValues.scollbar_handle_color
    border:str = DefaultConfigValues.scrollbar_border_color

class Scrollbar(BaseModel):
    color: ScrollbarColor = Field(default_factory = ScrollbarColor)
    

class SortBy(BaseModel):
    appid: bool = DefaultConfigValues.sort_by_appid
    custom: bool = DefaultConfigValues.sort_by_custom

class Games(BaseModel):
    exclude:   list[str | int | None] = []
    only_show: list[str | int | None] = []
    
    hide_steamworks_common_redistributables: bool = DefaultConfigValues.hide_steamworks_commmon

class Config(BaseModel):
    main_window: MainWindow = Field(default_factory = MainWindow)
    scrollbar: Scrollbar = Field(default_factory = Scrollbar)
    sort_by: SortBy = Field(default_factory = SortBy)
    games: Games = Field(default_factory = Games)
    
# == User Data ==

class GetGameIcons(BaseModel):
    hashes_to_ignore: list[str | None] = Field(default_factory=lambda: list(DefaultUserDataValues.hashes_to_ignore))
    ignore_unkown_hashes: bool = DefaultUserDataValues.ignore_unkown_hashes
    source: Literal["auto", "online", "offline"] = "auto"


class UserData(BaseModel):
    steam_path: str = DefaultUserDataValues.steam_path
    api_key: str = DefaultUserDataValues.api_key
    profile_id: str = DefaultUserDataValues.profile_id
    
    get_game_icons: GetGameIcons = Field(default_factory = GetGameIcons)
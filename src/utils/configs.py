import logging
from typing import Literal

from pydantic import (
    BaseModel,
    Field,
    NegativeInt,
    PositiveInt,
    field_validator,
    model_validator,
)

from .constants import DefaultConfigValues, DefaultUserDataValues

logger = logging.getLogger()
# == CONFIG ==


class Position(BaseModel):
    x: int | None = DefaultConfigValues.window_x_pos
    y: int | None = DefaultConfigValues.window_y_pos


class Size(BaseModel):
    width: int | None = DefaultConfigValues.window_widht
    height: int | None = DefaultConfigValues.window_height


class Font(BaseModel):
    family: str = DefaultConfigValues.window_font_family
    size: int = DefaultConfigValues.window_font_size


class MainWindow(BaseModel):
    title: str = DefaultConfigValues.window_title
    background: str = DefaultConfigValues.window_background
    foreground: str = DefaultConfigValues.window_foreground

    position: Position = Field(default_factory=Position)
    size: Size = Field(default_factory=Size)
    font: Font = Field(default_factory=Font)
    size_of_images: int | None = DefaultConfigValues.window_img_size


class ScrollbarColor(BaseModel):
    background: str = DefaultConfigValues.scollbar_background
    handle: str = DefaultConfigValues.scollbar_handle_color
    border: str = DefaultConfigValues.scrollbar_border_color


class Scrollbar(BaseModel):
    color: ScrollbarColor = Field(default_factory=ScrollbarColor)


class SortBy(BaseModel):
    appid: bool = DefaultConfigValues.sort_by_appid
    custom: bool = DefaultConfigValues.sort_by_custom


class Games(BaseModel):
    exclude: list[str | int] = []
    only_show: list[str | int] = []

    hide_steamworks_common_redistributables: bool = (
        DefaultConfigValues.hide_steamworks_commmon
    )

    @field_validator("exclude", "only_show", mode="before")
    @classmethod
    def remove_empty_hashes(cls, value):
        if value is None:
            return []

        return [game for game in value if game is not None]


class Config(BaseModel):
    main_window: MainWindow = Field(default_factory=MainWindow)
    scrollbar: Scrollbar = Field(default_factory=Scrollbar)
    sort_by: SortBy = Field(default_factory=SortBy)
    games: Games = Field(default_factory=Games)


# == User Data ==


class GetGameIcons(BaseModel):
    hashes_to_ignore: list[str] = Field(
        default_factory=lambda: list(DefaultUserDataValues.hashes_to_ignore)
    )
    ignore_unkown_hashes: bool = DefaultUserDataValues.ignore_unkown_hashes
    source: Literal["auto", "online", "offline"] = "auto"

    @field_validator("hashes_to_ignore", mode="before")
    @classmethod
    def remove_empty_hashes(cls, value):
        if value is None:
            return []

        return [unknown_hash for unknown_hash in value if unknown_hash is not None]


class CustomGame(BaseModel):
    name: str
    appid: NegativeInt
    exe_path: str


class SteamGame(BaseModel):
    name: str | None = None
    appid: PositiveInt | None = None
    exe_path: str

    @model_validator(mode="after")
    def validate_name_or_appid(self):
        if not self.name and not self.appid:
            raise ValueError('Either "name" or "appid" must be provided')
        return self


class UserData(BaseModel):
    steam_path: str = DefaultUserDataValues.steam_path
    api_key: str = DefaultUserDataValues.api_key
    profile_id: str = DefaultUserDataValues.profile_id

    steam_games: list[SteamGame] | None = []
    custom_games: list[CustomGame] | None = []

    get_game_icons: GetGameIcons = Field(default_factory=GetGameIcons)

    @field_validator("steam_games", "custom_games", mode="before")
    @classmethod
    def remove_empty_games(cls, value):
        if value is None:
            return []

        return [game for game in value if game is not None]

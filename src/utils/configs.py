import logging
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    NegativeInt,
    PositiveInt,
    field_validator,
    model_validator,
)

from .constants import ConfigValues, UserDataValues

logger = logging.getLogger()
# == CONFIG ==


class MyBaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class Position(MyBaseModel):
    x: int | None = ConfigValues.window_x_pos.pydantic_field()
    y: int | None = ConfigValues.window_y_pos.pydantic_field()


class Size(MyBaseModel):
    width: int | None = ConfigValues.window_width.pydantic_field()
    height: int | None = ConfigValues.window_height.pydantic_field()


class Font(MyBaseModel):
    family: str = ConfigValues.font_family.pydantic_field()
    size: int = ConfigValues.font_size.pydantic_field()


class MainWindow(MyBaseModel):
    title: str = ConfigValues.window_title.pydantic_field()
    background: str = ConfigValues.window_background.pydantic_field()
    foreground: str = ConfigValues.window_foreground.pydantic_field()

    position: Position = Field(
        default_factory=Position, alias=ConfigValues.window_position.yaml_key
    )
    size: Size = Field(default_factory=Size, alias=ConfigValues.window_size.yaml_key)
    font: Font = Field(default_factory=Font, alias=ConfigValues.window_font.yaml_key)
    size_of_images: int | None = ConfigValues.window_img_size.pydantic_field()


class ScrollbarColor(MyBaseModel):
    background: str = ConfigValues.scrollbar_color_background.pydantic_field()
    handle: str = ConfigValues.scrollbar_color_handle.pydantic_field()
    border: str = ConfigValues.scrollbar_color_border.pydantic_field()


class Scrollbar(MyBaseModel):
    scrollbar_off: bool = ConfigValues.scrollbar_off.pydantic_field()
    custom_scrollbar: bool = ConfigValues.scrollbar_custom.pydantic_field()
    color: ScrollbarColor = Field(
        default_factory=ScrollbarColor, alias=ConfigValues.scrollbar_color.yaml_key
    )


class SortBy(MyBaseModel):
    appid: bool = ConfigValues.sort_by_appid.pydantic_field()
    custom: bool = ConfigValues.sort_by_custom.pydantic_field()


class Games(MyBaseModel):
    exclude: list[str | int] = ConfigValues.games_exclude.pydantic_field()
    only_show: list[str | int] = ConfigValues.games_show_only.pydantic_field()

    hide_steamworks_common_redistributables: bool = (
        ConfigValues.games_hide_steamworks.pydantic_field()
    )

    @field_validator("exclude", "only_show", mode="before")
    @classmethod
    def remove_empty_hashes(cls, value):
        if value is None:
            return []

        return [game for game in value if game is not None]


class Config(MyBaseModel):
    main_window: MainWindow = Field(
        default_factory=MainWindow, alias=ConfigValues.main_window.yaml_key
    )
    scrollbar: Scrollbar = Field(
        default_factory=Scrollbar, alias=ConfigValues.scrollbar.yaml_key
    )
    sort_by: SortBy = Field(default_factory=SortBy, alias=ConfigValues.sort_by.yaml_key)
    games: Games = Field(default_factory=Games, alias=ConfigValues.games.yaml_key)


# == User Data ==


class GetGameIcons(MyBaseModel):
    hashes_to_ignore: list[str] = UserDataValues.hashes_to_ignore.pydantic_field()
    ignore_unkown_hashes: bool = UserDataValues.ignore_unkown_hashes.pydantic_field()
    source: Literal["auto", "online", "offline"] = (
        UserDataValues.source.pydantic_field()
    )

    @field_validator("hashes_to_ignore", mode="before")
    @classmethod
    def remove_empty_hashes(cls, value):
        if value is None:
            return []

        return [unknown_hash for unknown_hash in value if unknown_hash is not None]


class CustomGame(MyBaseModel):
    name: str = UserDataValues.custom_games_name.pydantic_field()
    appid: NegativeInt = UserDataValues.custom_games_appid.pydantic_field()
    exe_path: str = UserDataValues.custom_games_exe_path.pydantic_field()


class SteamGame(MyBaseModel):
    name: str | None = UserDataValues.steam_games_name.pydantic_field()
    appid: PositiveInt | None = UserDataValues.steam_games_appid.pydantic_field()
    exe_path: str

    @model_validator(mode="after")
    def validate_name_or_appid(self):
        if not self.name and not self.appid:
            raise ValueError('Either "name" or "appid" must be provided')
        return self


class UserData(MyBaseModel):
    steam_path: str = UserDataValues.steam_path.pydantic_field()
    api_key: str = UserDataValues.api_key.pydantic_field()
    profile_id: str = UserDataValues.profile_id.pydantic_field()

    steam_games: list[SteamGame] | None = UserDataValues.steam_games.pydantic_field()
    custom_games: list[CustomGame] | None = UserDataValues.custom_games.pydantic_field()

    get_game_icons: GetGameIcons = Field(
        default_factory=GetGameIcons, alias=UserDataValues.get_game_icons.yaml_key
    )

    @field_validator("steam_games", "custom_games", mode="before")
    @classmethod
    def remove_empty_games(cls, value):
        if value is None:
            return []

        return [game for game in value if game is not None]

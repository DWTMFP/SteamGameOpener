import logging
import sys
import webbrowser
from collections.abc import Iterable
from pathlib import Path

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont, QPalette
from PySide6.QtWidgets import (
    QAbstractItemView,
    QAbstractScrollArea,
    QApplication,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from utils import (
    STANDARD_CONFIG_PATH,
    Config,
    Game,
    Scrollbar,
    SteamGameManager,
    UserData,
    create_config,
    create_user_data,
    get_config,
    get_icon_from_appid,
    get_images,
    get_QScrollBar_style_sheet,
    get_user_data,
    run_exe,
)
from utils import Font as Config_Font
from utils import MainWindow as Config_MainWindow

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class ChooseExe(QWidget):
    def __init__(
        self,
        scrollbar: Scrollbar,
        font: Config_Font,
        item: QListWidgetItem,
        icon_size: QSize,
        exes: Iterable[Path],
    ):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        main_layout = QVBoxLayout()
        lbl_layout = QHBoxLayout()
        selection_layout = QHBoxLayout()

        # == Top Line ==
        self.img_lbl = QLabel()
        if not item.icon().isNull():
            self.img_lbl.setPixmap(item.icon().pixmap(icon_size))

        lbl_layout.addStretch()
        lbl_layout.addWidget(QLabel("Please choose the correct exe for:\t"))
        lbl_layout.addWidget(self.img_lbl)
        lbl_layout.addWidget(QLabel(item.text()))
        lbl_layout.addStretch()

        # == Button ==
        start_exe_btn = QPushButton("Run Exe")
        start_exe_btn.clicked.connect(self.on_run_exe)

        # == Exe Selection ==
        exe_selection = QListWidget()
        exe_selection.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        exe_selection.setStyleSheet(get_QScrollBar_style_sheet(scrollbar.color))
        exe_selection.setIconSize(icon_size)
        exe_selection.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )
        exe_selection.setFont(QFont(font.family, font.size))

        # == Add Exes ==
        for exe in exes:
            exe_selection.addItem(str(exe))

        self.exe_selection = exe_selection

        # == Add Layouts, and Widgets and set Layout ==
        selection_layout.addWidget(start_exe_btn)
        selection_layout.addWidget(exe_selection)

        main_layout.addLayout(lbl_layout)
        main_layout.addLayout(selection_layout)
        self.setLayout(main_layout)

    def on_run_exe(self):
        current_item = self.exe_selection.currentItem()
        if current_item is None:
            return
        exe_path = current_item.text()
        run_exe(Path(exe_path))


class MainWindow(QMainWindow):
    def __init__(self, config: Config, user_data: UserData):  # noqa: PLR0915
        super().__init__()

        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self.steam_data = SteamGameManager(user_data)
        self.user_data = user_data
        self.config = config

        games_to_exclude = config.games.exclude
        if config.games.hide_steamworks_common_redistributables:
            games_to_exclude.append("Steamworks Common Redistributables")
        self.games_to_exclude = games_to_exclude
        self.only_these_games = config.games.only_show

        # ============
        # == Layout ==
        # ============

        self.setWindowTitle(config.main_window.title)

        x_pos = config.main_window.position.x
        y_pos = config.main_window.position.y

        if x_pos is not None or y_pos is not None:
            self.move(
                x_pos if x_pos is not None else 0,
                y_pos if y_pos is not None else 0,
            )

        width = config.main_window.size.width
        height = config.main_window.size.height

        self.img_size = config.main_window.size_of_images
        self.sort_by = config.sort_by
        self.games = config.games

        main_layout = QHBoxLayout()
        main_layout.setSpacing(10)

        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)

        run_game_btn = QPushButton("Run Game")
        run_game_btn.clicked.connect(self.on_run_game)

        self.via_weburl = True
        self.via_exe_btn = QPushButton("Via Weburl")
        self.via_exe_btn.clicked.connect(self.on_via_exe_btn)

        update_btn = QPushButton("Update")
        update_btn.clicked.connect(self.on_update)

        button_layout.addStretch()  # Stretch for widgets to stay togther when resizing the window
        button_layout.addWidget(QLabel("Which Game do you want to play?"))
        button_layout.addWidget(run_game_btn)
        button_layout.addWidget(self.via_exe_btn)
        button_layout.addWidget(update_btn)
        button_layout.addStretch()

        self.games_widget = QListWidget()
        self.games_widget.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        if not config.scrollbar.custom_scrollbar:
            self.games_widget.setStyleSheet(
                get_QScrollBar_style_sheet(config.scrollbar.color)
            )
        if self.img_size is not None:
            self.games_widget.setIconSize(QSize(self.img_size, self.img_size))
        self.games_widget.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )
        self.games_widget.setFont(
            QFont(config.main_window.font.family, config.main_window.font.size)
        )
        self.games_widget.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        if config.scrollbar.scrollbar_off:
            self.games_widget.setHorizontalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOff
            )

        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.games_widget, stretch=1)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.add_games()

        if width is not None or height is not None:
            size = self.size()

            if width is not None:
                size.setWidth(width)

            if height is not None:
                size.setHeight(height)

            self.resize(size)
        else:
            self.adjustSize()

    def add_games(self):
        self.games_widget.clear()

        only_these_games = self.only_these_games
        exclude_these_games = self.games_to_exclude

        listed_games = self.steam_data.get_listed_games()
        if self.sort_by.appid:
            listed_games.sort(key=lambda game: game.appid)

        for game in listed_games:
            game_name = game.name
            appid = game.appid

            if (
                only_these_games
                and game_name not in only_these_games
                and appid not in only_these_games
            ) or (
                exclude_these_games
                and (game_name in exclude_these_games or appid in exclude_these_games)
            ):
                continue

            icon = get_icon_from_appid(appid)

            if icon is not None:
                item = QListWidgetItem(icon, game_name)
            else:
                item = QListWidgetItem(game_name)

            item.setSizeHint(
                QSize(
                    self.games_widget.width(),
                    self.img_size + 10 if self.img_size is not None else 10,
                )
            )

            self.games_widget.addItem(item)

    def on_run_game(self):
        current_item = self.games_widget.currentItem()
        if current_item is None:
            return
        game = self.steam_data.get_game(game_name=current_item.text())
        if self.via_weburl:
            appid = game.appid
            if appid < 0:
                self.run_game_via_exe(game)
            # DO NOT REMOVE ELSE, OTHERWISE sys.exit() BREAKS EXE_SELECTION
            else:
                self.run_weburl(
                    rf"steam://rungameid/{self.steam_data.get_appid(game.name)}"
                )

        else:
            self.run_game_via_exe(game)

    def run_weburl(self, weburl: str):
        logger.info(f'Running "{weburl}"')
        webbrowser.open(weburl)
        sys.exit()

    def run_game_via_exe(self, game: Game):
        game = self.steam_data.get_game(game_name=game.name)
        steam_path = Path(self.user_data.steam_path)
        steamapps_common_path = steam_path / "steamapps" / "common"

        if game.appid >= 0:
            install_dir = steamapps_common_path / game.install_dir
        # keep that for legacy reasons
        else:
            install_dir = Path(game.install_dir)

        if game.exe_path is not None:
            logger.info(f"Found Exe Path specified. Working with {game.exe_path}")
            exe_path = Path(game.exe_path)
            if exe_path.is_absolute() and exe_path.exists():
                run_exe(exe_path)
            else:
                new_exe_path = steamapps_common_path / exe_path
                logger.info(
                    f'"{str(exe_path)}" was not found, now trying "{str(new_exe_path)}"'
                )
                if new_exe_path.exists():
                    run_exe(new_exe_path)
                logger.info(
                    "Also not found. Some Configuration was not setup correctly, defaulting to normal search."
                )

        if not install_dir.is_dir():
            logger.warning(
                f"The supposed install dir of {install_dir} from game: {game.name} is not a directory."
            )
            return

        exe_to_try = install_dir / (game.name + ".exe")
        logger.info(f'Checking if "{exe_to_try}" exists')
        if exe_to_try in install_dir.glob("*.exe"):
            run_exe(exe_to_try)

        # Now install_dir is a valid directory, without game_name.exe, so check for other exe in that dir, with subdirs
        logger.info(
            "Doesn't exist. Now searching for exes in Path, and trying similiar one"
        )
        all_exes_iterator = set(install_dir.rglob("*.exe", case_sensitive=False))
        for exe in all_exes_iterator:
            if self.normalize_exe(exe.stem) == self.normalize_exe(game.name):
                run_exe(exe)

        # Didn't work either
        logger.info("Giving up to autodetect, now choose yourself.")

        self.exe_chooser = ChooseExe(
            self.config.scrollbar,
            self.config.main_window.font,
            self.games_widget.currentItem(),
            self.games_widget.iconSize(),
            all_exes_iterator,
        )
        self.exe_chooser.show()

    def normalize_exe(self, s: str) -> str:
        return s.lower().replace(" ", "").replace("_", "")

    def on_update(self):
        self.steam_data.write_games_to_txt()
        get_images(self.user_data)
        self.add_games()

    def on_via_exe_btn(self):
        if self.via_exe_btn.text() == "Via Weburl":
            self.via_exe_btn.setText("Via Exe")
        else:
            self.via_exe_btn.setText("Via Weburl")
        self.via_weburl = not self.via_weburl


class GameAppidGUI(QMainWindow):
    def __init__(self, user_data: UserData, config: Config):
        super().__init__()
        self.steam_manager = SteamGameManager(user_data)
        list_widget = QListWidget()

        img_size = config.main_window.size_of_images

        list_widget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        list_widget.setStyleSheet(get_QScrollBar_style_sheet(config.scrollbar.color))
        if img_size is not None:
            list_widget.setIconSize(QSize(img_size, img_size))
        list_widget.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )
        list_widget.setFont(
            QFont(config.main_window.font.family, config.main_window.font.size)
        )
        list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        items_with_image: list[QListWidgetItem] = []
        items_without_image: list[QListWidgetItem] = []
        all_games = self.steam_manager.get_all_games()
        for game in sorted(all_games, key=lambda game: game.appid):
            display_str = f"{game.name}: {game.appid}"
            print(display_str)

            icon = get_icon_from_appid(game.appid)

            if icon is not None:
                item = QListWidgetItem(icon, display_str)
                items_with_image.append(item)
            else:
                item = QListWidgetItem(display_str)
                items_without_image.append(item)

            item.setData(Qt.ItemDataRole.UserRole, game.appid)

        for item in items_without_image:
            list_widget.addItem(item)
        for item in items_with_image:
            list_widget.addItem(item)

        list_widget.itemClicked.connect(self.copy_appid_to_clipboard)
        self.setCentralWidget(list_widget)
        self.adjustSize()

    def copy_appid_to_clipboard(self, item: QListWidgetItem):
        appid = item.data(Qt.ItemDataRole.UserRole)
        logger.info(
            f'Copying AppID: "{appid}" from Game: "{self.steam_manager.get_game_name(appid)}" to Clipboard'
        )
        QApplication.clipboard().setText(str(appid))


def set_app_config(app: QApplication, main_window: Config_MainWindow):
    app.setFont(QFont(main_window.font.family, main_window.font.size))

    palette = app.palette()

    # set background color
    for role in (
        QPalette.ColorRole.Window,
        QPalette.ColorRole.Base,
        QPalette.ColorRole.Button,
        QPalette.ColorRole.Highlight,
    ):
        palette.setColor(role, main_window.background)

    # set foreground color
    for role in (
        QPalette.ColorRole.WindowText,
        QPalette.ColorRole.Text,
        QPalette.ColorRole.ButtonText,
    ):
        palette.setColor(role, main_window.foreground)

    app.setPalette(palette)


def display_game_appid(config_path: Path):
    app = QApplication()
    config = get_config(config_path)
    user_data = get_user_data()

    set_app_config(app, config.main_window)

    gui = GameAppidGUI(user_data, config)
    gui.show()
    app.exec()


def display_gui(config_path: Path):
    config = get_config(config_path)
    user_data = get_user_data()

    app = QApplication()
    set_app_config(app, config.main_window)

    window = MainWindow(config, user_data)
    window.show()
    app.exec()


if __name__ == "__main__":
    create_config()
    create_user_data()
    display_gui(STANDARD_CONFIG_PATH)

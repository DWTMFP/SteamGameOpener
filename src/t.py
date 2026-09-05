from pathlib import Path

from utils import SteamGameManager, get_user_data

print(*SteamGameManager(get_user_data()).get_all_games(), sep="\n")

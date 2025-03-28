from helper import Helper

def main():
    helper = Helper()
    appids = helper.get_appids()
    appids.sort(key = int)
    games = helper.get_game_names_and_install_dirs(appids)[0]
    for i in range(len(games)):
        print(f"{games[i]}: {appids[i]}")

if __name__ == "__main__":
    main()
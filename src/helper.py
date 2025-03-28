import os
import requests


import user_data



class Helper():
    CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    appids = None
    
    def get_appids(self):
        #in the Steam\steamapps folder there are appmanifest_{appid}.acf files of all steam games, which are installed locally
        folder = os.listdir(user_data.PATH_TO_STEAM.removesuffix("\\")+r"\steamapps")
        
        appids:list[str] = [] 

        for file in folder:
            if file.startswith("appmanifest_"):
                appids.append(file.removeprefix("appmanifest_").removesuffix(".acf"))
                
        self.appids = appids
        return appids


    def get_used_appids(self):
        used_appids = []
        path_to_images = os.path.join(self.CURRENT_DIRECTORY, r'.\images')
        if os.path.exists(path_to_images):
            for element in os.listdir(path_to_images):
                used_appids.append(element.replace(".jpg", ""))

        self.used_appids = used_appids    
        return used_appids
    
    def get_game_names_and_install_dirs(self, appids:list[str]):
        game_names = []
        install_dirs = []
        for appid in appids:
            file = user_data.PATH_TO_STEAM + fr"\steamapps\appmanifest_{appid}.acf"
            with open(file) as f:
                text = f.read()
                
            text = text.split("\n")
            
            for line in text:
                line = line.replace("\t","").replace("\"","")
                if line.startswith("name"):
                    game_names.append(line.replace("name",""))
                if line.startswith("installdir"):
                    install_dirs.append(line.replace("installdir",""))
        self.games = game_names

        return game_names, install_dirs


    def create_dict(self, keys:list[str], values:list[str]):
        d = {}
        for i in range(len(keys)):
            d[keys[i]] = values[i]
        return d



    def download_image(self, image_url, file_dir):
        response = requests.get(image_url)

        if response.status_code == 200:
            directory = os.path.dirname(file_dir)
            if not os.path.exists(directory):
                os.makedirs(directory)

            with open(file_dir, "wb") as fp:
                fp.write(response.content)


    def create_imgs(self):
        appids = self.appids
        used_appids = self.get_used_appids()


        if used_appids != []:
            for used_appid in used_appids:
                appids.remove(used_appid)

        
        game_icons = dict()

        
        result = requests.get(f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={user_data.STEAM_API_KEY}&steamid={user_data.STEAM_PROFILE_ID}&format=json&include_played_free_games=1&include_appinfo=1&skip_unvetted_apps=false&include_free_sub").json()['response']
        if 'games' not in result:
            print("failed")

        for game in result['games']:
            game_icons[str(game['appid'])] = game['img_icon_url']

        for appid in appids:
            try:
                img = f"http://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{game_icons[appid]}.jpg"
                self.download_image(img, os.path.join(self.CURRENT_DIRECTORY, rf'.\images\{appid}.jpg'))
            except Exception as e:
                print(e)
    
    def remove_leading_whitespaces_and_tabs(self, s:str):
        for i in range(len(s)):
            if s.startswith(" "):
                s = s[1:]
            else:
                break
        return s
    
    def get_games(self):
        if self.appids != None:
            return self.get_game_names_and_install_dirs(self.appids)[0]
        else:
            appids = self.get_appids()
            return self.get_game_names_and_install_dirs(appids)[0]
            
    
    def get_games_from_txt(self):
        "gets games, which are in games.txt"
        with open(self.CURRENT_DIRECTORY+r"\games.txt") as file:
            text = file.read()
            text = text.split("\n")
        games:list[str] = []
        for line in text:
            if line.replace(" ","").replace("\t","")=="": continue
            games.append(line)
        return games
    
    def reorder_game_names(self, game_names):
        if not os.listdir(self.CURRENT_DIRECTORY).__contains__("games.txt"):
            return game_names
        
        sorted_games = self.get_games_from_txt() 
        for sorted_game in sorted_games:
            if sorted_game not in game_names:
                sorted_games.remove(sorted_game)
        
        return sorted_games
        
        
    def reorder_appids(self, games, games_appids):
        return [games_appids[game] for game in games]
    
    def reorder_install_dirs(self, games, games_install_dir):
        return [games_install_dir[game] for game in games]
    
    def write_games_to_txt(self):
        games = self.games
        s=str()
        for game in games:
            s+=game + "\n"
        with open(self.CURRENT_DIRECTORY + r"\games.txt", "w") as file:
            file.write(s)
    
    def write_new_games_to_txt(self):
        games = self.games
        s=str()
        old_games = self.get_games_from_txt()
        new_games = [game for game in games if game not in old_games] #[games] - [old_games]
        
        for old_game in old_games:
            s += old_game + "\n"
            
        for new_game in new_games:
            s += new_game + "\n"
        
        with open(self.CURRENT_DIRECTORY + r"\games.txt", "w") as file:
            file.write(s)
        

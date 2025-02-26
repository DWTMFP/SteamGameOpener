import os
import requests


import user_data



class Helper():
    def __init__(self, hide_weird_app):
        self.hide_weird_app = hide_weird_app #weird app = STEAM_COMMON_REDISTRIBUTABLE
    CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    
    
    def get_appids(self):
        #in the Steam\steamapps folder there are appmanifest_{appid}.acf files of all steam games, which are installed locally
        folder = os.listdir(user_data.PATH_TO_STEAM.removesuffix("\\")+r"\steamapps")
        
        appids_not_usable:list[str] = [] #not usable, because they will contain rest of the file name
        appids:list[str] = [] 

        for file in folder:
            if file.startswith("appmanifest_"):
                appids_not_usable.append(file)

        for appid in appids_not_usable:
            appids.append(appid.removeprefix("appmanifest_").removesuffix(".acf"))

        if os.listdir().__contains__("appmanifest_228980.acf") and self.hide_weird_app:
            appids.remove("228980")


        return appids


    def get_used_appids(self):
        used_appids = []
        path_to_images = os.path.join(self.CURRENT_DIRECTORY, r'.\images')
        if os.path.exists(path_to_images):
            for element in os.listdir(path_to_images):
                used_appids.append(element.replace(".jpg", ""))

            
        return used_appids
                                    

    def get_game_name_from_appid(self, appid):
        file = user_data.PATH_TO_STEAM + fr"\steamapps\appmanifest_{appid}.acf"
        with open(file) as f:
            text = f.read()
            
        text = text.split("\n")
        
        for line in text:
            line = line.replace("\t","").replace("\"","")
            if line.startswith("name"):
                return line.replace("name","")


    def get_games_appids_dict(self, appids:list[str]) -> dict[str:str]:
        '''
        The dictionary will have the app names as keys and the appids as values
        '''
        games_appids_dict:dict[str:str] = {} #dictionary with app names as keys and appids as values
        
        for appid in appids:
            games_appids_dict[self.get_game_name_from_appid(appid)] = appid
        
        return games_appids_dict


    def get_appids_games_dict(self, appids:list[str]) -> dict[str:str]:
        appids_games_dict = {}
        
        for appid in appids:
            appids_games_dict[appid] = self.get_game_name_from_appid(appid)
        
        return appids_games_dict



    def download_image(self, image_url, file_dir):
        response = requests.get(image_url)

        if response.status_code == 200:
            directory = os.path.dirname(file_dir)
            if not os.path.exists(directory):
                os.makedirs(directory)

            with open(file_dir, "wb") as fp:
                fp.write(response.content)


    def create_imgs(self):
        appids = self.get_appids()
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
            except:
                pass
    
    def remove_leading_whitespaces_and_tabs(self, s:str):
        for i in range(len(s)):
            if s.startswith(" "):
                s = s[1:]
            else:
                break
        return s
    
    def get_games(self):
        games = []
        appids = self.get_appids()
        for appid in appids:
            games.append(self.get_game_name_from_appid(appid))
        return games
    
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
    
    
    def write_games_to_txt(self):
        games = self.get_games()
        s=str()
        for game in games:
            s+=game + "\n"
        with open(self.CURRENT_DIRECTORY + r"\games.txt", "w") as file:
            file.write(s)
    
    def write_new_games_to_txt(self):
        games = self.get_games()
        s=str()
        old_games = self.get_games_from_txt()
        new_games = [game for game in games if game not in old_games] #[games] - [old_games]
        
        for old_game in old_games:
            s += old_game + "\n"
            
        for new_game in new_games:
            s += new_game + "\n"
        
        with open(self.CURRENT_DIRECTORY + r"\games.txt", "w") as file:
            file.write(s)
        

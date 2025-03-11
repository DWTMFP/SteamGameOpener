import tkinter as tk
import os
import sys
import webbrowser
from helper import Helper
from PIL import ImageTk, Image
from copy import deepcopy


import user_data




class window():
    master:tk.Tk
    std_font:list
    web_url = True
    
    def __init__(self, master:tk.Tk, user_config):
        self.user_config = user_config
        self.helper = Helper()
        
        #create games.txt, for custom sorting
        if not os.listdir(self.helper.CURRENT_DIRECTORY).__contains__("games.txt"):
            self.helper.write_games_to_txt()

        
        self.create_complete_dicts()

        #for sorting the games in the order, in which they are saved in the games.txt file
        if self.user_config.ONLY_SHOW_THESE_GAMES != []:
            self.show_certain_games()
        else:
            self.exclude_games() #in else, because ``ONLY_SHOW_THESE_GAMES`` is supposed to overwrite
        
        
        if self.user_config.SORT_BY_CUSTOM_ORDER:
            self.create_new_dicts()
        
        #create standard values and the window itself
        self.master = master
        self.std_font = self.user_config.STANDARD_FONT
        self.std_font_underline = deepcopy(self.user_config.STANDARD_FONT)
        self.std_font_underline.append("underline")

        self.start_frame = tk.Frame(self.master)
        self.start_frame.grid(row = 0, column = 0, padx = 15)
        
        self.create_scrollable_frame()
        
              
        self.choose_game_label = tk.Label(self.start_frame, text = "Which Game do you want to play?", font = self.std_font)
        self.choose_game_label.grid(row = 0, column = 0)
        
        self.start_game_btn = tk.Button(self.start_frame, text = "Run Game", command = self.run_game, font = self.std_font).grid(row = 1, column = 0)
        self.update_btn = tk.Button(self.start_frame, text = "update", command = self.update, font = self.std_font).grid(row = 3, column = 0)
        self.toggle_how_to_open_btn = tk.Button(self.start_frame, text = "Via WebUrl", command = self.toggle_how_to_open_fn, font = self.std_font)
        self.toggle_how_to_open_btn.grid(row = 2, column = 0)

        
        self.add_games()
        
        #autoselect the first game
        self.last_pressed_label = self.labels_dict[self.appids[0]]
        self.last_pressed_label.config(font = self.std_font_underline)
    
    
    def create_scrollable_frame(self):
        self.choose_game_frame_master = tk.Frame(self.master)#master, so i can put the actual frame in it (to enable scrolling)
        self.choose_game_frame_master.grid(row = 0, column = 1)
        
        self.choose_game_canvas = tk.Canvas(self.choose_game_frame_master)
        self.choose_game_canvas.pack(side = "left")
        
        self.choose_game_frame = tk.Frame(self.choose_game_canvas)

        
        self.choose_game_scrollbar = tk.Scrollbar(self.choose_game_frame_master, orient = "vertical", command=self.choose_game_canvas.yview)
        self.choose_game_scrollbar.pack(side = "right", fill = "y")
        
        self.choose_game_canvas.config(yscrollcommand = self.choose_game_scrollbar.set)
        self.choose_game_canvas.create_window((0,0), window = self.choose_game_frame, anchor='nw')
        
        self.choose_game_frame.bind("<Configure>", self.scroll)
        
        
    
    def show_certain_games(self):
        new_appids = []
        new_games_appids = {}
        new_appids_games = {}
        for game in self.user_config.ONLY_SHOW_THESE_GAMES:
            appid = self.games_appids[game]
            new_appids.append(appid)
            new_games_appids[game] = appid
            new_appids_games[appid] = game

        
        self.games_appids = new_games_appids
        self.appids_games = new_appids_games
        self.appids = new_appids
        
    
    def exclude_games(self):
        for game in self.user_config.GAMES_TO_EXCLUDE:
            appid = self.games_appids[game]
            self.games_appids.pop(game)
            self.appids_games.pop(appid)
            self.appids.remove(appid)
        if os.listdir(user_data.PATH_TO_STEAM.removesuffix("\\")+r"\steamapps").__contains__("appmanifest_228980.acf") and self.user_config.HIDE_STEAMWORKS_COMMON_REDISTRIBUTABLES:
            self.games_appids.pop("Steamworks Common Redistributables")
            self.appids_games.pop("228980")
            self.appids.remove("228980")
            
    
    def create_new_dicts(self):
        #get name of all games, in the file
        with open(self.helper.CURRENT_DIRECTORY + r"\games.txt") as file:
            text = file.read()
        text = text.split("\n")
        
        self.create_complete_dicts()
        
        games = self.helper.get_games_from_txt()
        new_games_appids_dict = {}
        new_appids_games_dict = {}
        new_appids = []
        for game in games:
            new_games_appids_dict[game] = self.games_appids[game]
            new_appids_games_dict[self.games_appids[game]] = game
            new_appids.append(self.games_appids[game])
        
        self.games_appids = new_games_appids_dict
        self.appids_games = new_appids_games_dict
        self.appids = new_appids

        if self.user_config.ONLY_SHOW_THESE_GAMES != []:
            self.show_certain_games()
        else:
            self.exclude_games() #in else, because ``ONLY_SHOW_THESE_GAMES`` is supposed to overwrite
        
        

    def create_complete_dicts(self):
        self.appids = self.helper.get_appids()
        
        if self.user_config.SORT_BY_APPID:
            self.appids.sort(key = int) #sort them by appid, key = int is because they are strings, which should be sorted like strings
        
        self.games_appids:dict = self.helper.get_games_appids_dict(self.appids)
        self.appids_games:dict = self.helper.get_appids_games_dict(self.appids)
    
    
    def toggle_how_to_open_fn(self):
        if self.web_url:
            self.toggle_how_to_open_btn.config(text = "Via Exe")
            self.web_url = False
        else:
            self.toggle_how_to_open_btn.config(text = "Via WebUrl")
            self.web_url = True
        
        
        
    def add_games(self):
        self.labels_dict = {}
        CURRENT_DIRECTORY = self.helper.CURRENT_DIRECTORY
        img_dir_empty = True
        if os.listdir(CURRENT_DIRECTORY).__contains__("images"):
            img_dir = CURRENT_DIRECTORY + "\\images"
            if os.listdir(img_dir) != []:
                img_dir_empty = False
                imgs = os.listdir(img_dir)
        
        #make class vars to local vars (I hope this increases performance)
        appids = self.appids
        labels_dict = self.labels_dict
        appids_games = self.appids_games
        std_font = self.std_font
        size_of_images = self.user_config.SIZE_OF_IMAGES
        size_of_images = [size_of_images, size_of_images]
        
        
        if not img_dir_empty:
            for i in range(len(appids)):
                current_appid = appids[i]
                text_for_label:str = " " + appids_games[appids[i]]
                
                if imgs.__contains__(current_appid+".jpg"):
                    img = Image.open(img_dir+"\\"+current_appid+".jpg")
                    img.resize(size_of_images)
                    img = ImageTk.PhotoImage(img)
                    labels_dict[current_appid] = tk.Label(self.choose_game_frame, text = text_for_label,
                                                                image = img, font = std_font, compound = "left") #compund means the img is left of the text
                    labels_dict[current_appid].image = img
                    


                else: #if no img was used for this appid, add the game, without it
                    labels_dict[current_appid] = tk.Label(self.choose_game_frame, text = text_for_label,
                                                            font = std_font, compound = "left") #no height, because tkinter doesn't like that; don't ask why
                labels_dict[current_appid].bind(f"<Button-1>", lambda button = labels_dict[current_appid]: self.update_selected_game(button))
                labels_dict[current_appid].grid(row = i, column = 0, sticky = "w")
                        
        else:
            for i in range(len(appids)):
                current_appid = appids[i]
                text_for_label = appids_games[appids[i]]
                
                labels_dict[current_appid] = tk.Label(self.choose_game_frame, text = appids_games[current_appid],
                                                            font = std_font, compound = "left") #no height, because tkinter doesn't like that; don't ask why
                labels_dict[current_appid].bind(f"<Button-1>", lambda button = labels_dict[current_appid]: self.update_selected_game(button))
                labels_dict[current_appid].grid(row = i, column = 0, sticky = "w")

        self.labels_dict = labels_dict

            


    def update_selected_game(self, event):
        self.last_pressed_label.config(font = self.std_font)
        
        #the label is stored in img_labels_dict with the index of the appid; event.widget returns the widget, wich triggered the event (in this case, that it was pressed)
        #the .cget("text") just returns the text of the pressed label (the app_name); because that might start with whitspace characters (" "; "\t") they are getting removed
        #finally you get the needed appid by inserting the app_name into the dict, which then is the key to the dict storing the labels, returning the pressed label
        pressed_label:tk.Label = self.labels_dict[self.games_appids[self.helper.remove_leading_whitespaces_and_tabs(event.widget.cget("text"))]]
        pressed_label.config(font = self.std_font_underline)
        
        self.last_pressed_label = pressed_label



    def update(self):
        self.helper.create_imgs()
        self.helper.write_new_games_to_txt()
        self.create_new_dicts()
        self.add_games()
            
    
    def run_game(self):
        #app = self.games_listbox.get(self.games_listbox.curselection())
        app = self.last_pressed_label.cget("text")
        app = self.helper.remove_leading_whitespaces_and_tabs(app) #the app might start with a whitespace
        
        if not self.web_url:
            os.startfile(user_data.PATH_TO_STEAM + fr"\steamapps\common\{app}\{app}.exe")
        else:
            webbrowser.open(rf"steam://rungameid/{self.games_appids[app]}") #self.games_appids[app] is equivalent to the appid
        
        sys.exit()
    
    
    def scroll(self, event):
        self.choose_game_canvas.configure(scrollregion=self.choose_game_canvas.bbox("all"), height = self.user_config.HEIGHT_SCROLLBAR, width = self.user_config.WIDTH_SCROLLBAR)
        


def main(user_config):
    #define your root window
    root = tk.Tk()
    root.title(user_config.TITLE_OF_WINDOW)
    root.tk_setPalette(background = user_config.BACKGROUND_OF_WINDOW, foreground = user_config.FOREGROUND_OF_WINDOW)
    
    if user_config.WIDTH == None and user_config.HEIGHT == None:
        root.geometry(f"+{user_config.X_POS_OF_WINDOW}+{user_config.Y_POS_OF_WINDOW}")
    else:
        root.geometry(f"{user_config.WIDTH}x{user_config.HEIGHT}+{user_config.X_POS_OF_WINDOW}+{user_config.Y_POS_OF_WINDOW}")
    
    window(root, user_config)

    root.mainloop()



if __name__ == "__main__":
    if os.listdir().__contains__("user_config.py"):
        import user_config
        main(user_config)

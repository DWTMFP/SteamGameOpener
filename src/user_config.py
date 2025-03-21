#customise the window
TITLE_OF_WINDOW:str = "Steam Games" #std "Steam Games"
BACKGROUND_OF_WINDOW:str = "black" #std "black"
FOREGROUND_OF_WINDOW:str = "white" #std "white"

X_POS_OF_WINDOW:str = "0" #std "0"
Y_POS_OF_WINDOW:str = "0" #std "0"

HEIGHT_SCROLLBAR = 900 #std 600; It's the height of the Scrollbar in Pixels
WIDTH_SCROLLBAR = 525 #std 525
HEIGHT = None #std None; It's the height in pixels, of the window, can't drop below a certain size so the games are not being displayed of screen 
WIDTH = None #std None; only if both, HEIGHT and WIDTH are set to None, the window will choose the size it needs.

STANDARD_FONT:list = ["Arial", 20] #std ["Arial", 20]; font(str) and size(int); Must have two items in it

SIZE_OF_IMAGES:int = 31 #std 31

#sorting stuff
SORT_BY_APPID:bool = False #std False

'''
to change the order of games, go to the games.txt file (will be created, upon first start) and change the order of games there
you are allowed to insert lines without characters
also if you delete one game from there, it won't show up
but if you want to exclude a game from showing up, GAMES_TO_EXCLUDE is recommended, because the game will be readded, if you click on update
If you click on update, the games will be stored in new_games.txt, and you have to copy them from there to games.txt. In that way the old order won't get overwritten.
``SORT_BY_CUSTOM_ORDER`` takes priorisation over ``SORT_BY_APPID``
'''
SORT_BY_CUSTOM_ORDER:bool = True #std True


#others
HIDE_STEAMWORKS_COMMON_REDISTRIBUTABLES:bool = True #std True; Not a real game, therefore it won't be visible by default


GAMES_TO_EXCLUDE:list[str] = [] #std []; Values are game_names as strings
'''
this will override ``GAMES_TO_EXCLUDE``
it will display them in the order, in which they are in the list
'''
ONLY_SHOW_THESE_GAMES:list[str] = [] #std []; Values are game_names as strings

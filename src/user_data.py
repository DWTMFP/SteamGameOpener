'''
The Steam API Key and the Steam Profile ID are only needed, if you want to have the Icons of the Steam Games in the programm
The path to the steam installation is necessary, because from there the programm will get the appids and game names to start and insert them
'''


'''
The Path to the Steam folder
the given path is the standard path, if installed for all users
The last character doesn't need to be a backslash \
Insert the path between the apostrophes
'''
PATH_TO_STEAM = r"C:\Program Files (x86)\Steam" #std C:\Program Files (x86)\Steam



"""
You can only create a API Key, if you have spent money on Steam (as far as I know)
Create a Steam-Web-API-Key here 
http://steamcommunity.com/dev/apikey
Insert the Key between the apostrophes, e. g. 
STEAM_API_KEY = "akfj3akfp93q234ds9"
"""
STEAM_API_KEY = ""

"""
Your Steam Profile ID in 64-Bit
To look it up, go to Steam -> Settings; in the upper left corner there should appear link in the form of https://steamcommunity.com/profiles/48157112/
The number is your Profile ID; the one 
If you click on that link, it will copy to clipboard, making it easier for you to enter your ID here
Again insert it between the apostrophes
"""
STEAM_PROFILE_ID = ""



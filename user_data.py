'''
The Steam API Key and the Steam Profile ID are only needed, if you want to have the Icons of the Steam Games in the programm
The path to the steam installation is necessary, because from there the programm will get the appids and game names to start and insert them
Make sure that the Values are all within the apostrophes and make sure, that in front of the apostrophe of the steam path there is ONE r
'''


'''
The Path to the Steam folder
the given path is the standard path, if installed for all users
The last character doesn't need to be a backslash \ 
standard path for global installaion is "C:\Program Files (x86)\Steam"
'''
PATH_TO_STEAM = r"C:\Program Files (x86)\Steam"



"""
Create a Steam-Web-API-Key here http://steamcommunity.com/dev/apikey
and insert it between the apostrophes
"""
STEAM_API_KEY = ""

"""
Your Steam Profile ID in 64-Bit
To look it up, go to Steam -> Settings; in the upper left corner there should appear link in the form of https://steamcommunity.com/profiles/48157112/
The number is your Profile ID; the one 
If you click on that link, it will copy to clipboard, making it easier for you to enter your ID here
"""
STEAM_PROFILE_ID = ""





# SteamGameOpener

Creates a tkinter window, in which you choose the game you want to play and then opens it.

The reason behind this project was to free Space on my Desktop while still having the image icons next to  the game name.

This will be a step by step Guide, to set up everything - hopefully.

# Prerequisites
You need to have python installed on your computer.
I don't know, if the code runs on other Operating Systems than Windows, so yeah if your on Linux or Mac, Good Luck.


# Getting started
1. Download the files<br> since you only need the files in the src folder, you can delete the other files and extract all files from said folder
2. Open the user_data.py in a text or code editor
3. Fill in at least the path to steam, if you want images next to the names, you have to also insert your Steam API Key and your Steam Profile ID. This is because, in order to get the images the program uses the Steam API and for the API request, it needs these informations.<br>Please note, that this will not work for Games, which you have via family library, because it get's the images from your Steam Games, and Games which you have downloaded via family, are not in this list of games. (You can add those images manually, by Navigating to Steam\steam\games and then renaming the .ico to .jpg and saving in in the image directory, which will be created by this programm)
4. run run_Starter.bat
5. If it works, you can click on update (only, if you have entered the Steam API Key and your Steam Profile ID) and the Icons should appear (this takes a while)

- If you want to change for example the size or font of the text or the position, in which the window will appear go to user_config.py [go to Customizing for more details](#Customizing)
- You can have [different Instances](#Multiple%20Instances) of the application
  

The recommended use of the batch file is to, create a link to it (right click → create link) and then change the properties of the link, to start (run) minimized (right click → properties →  run). That way, only the python program opens, and the cmd window, which opens as well won't show up, because it is minimized and therefore only appears in the Task Bar.

# Customizing
To Configure anything you need to go to the user_config.py file

- The std means standard and is there to reset to default values if wanted
- Most of the used variable names are self-explanatory or the meaning behind them get's explained, so read those comments (anything behind a # is considered a comment)
- If you change the font size to be bigger, it might happen, that you need to increase the img_size (size of the images) as well
- You can use hex values for the colors.
- Steamworks Common Redistributables is not a game you can play, if you run it, steam will open, so it is hidden by default, but you might not have it.
- If you want to exclude certain games, insert them with apostrophes, separated with a comma in the brackets f. e. \["Game1", "Game2"]
- To only include certain games, do the same thing



## Multiple Instances

1. create a second user config file by saving the old one under a different name (the name is irrelevant, as long, as the file has a .py extension) and then configuring it .

2. also duplicate the batch file and change the command to (you have to replace "{name_of_your_config_file}" with well, the name of the new config file.):
   python main.py -cfg_file {name_of_your_config_file}
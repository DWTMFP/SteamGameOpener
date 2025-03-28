# SteamGameOpener

Creates a tkinter window, in which you choose the game you want to play and then opens it.

The reason behind this project was to free Space on my Desktop while still having the image icons next to  the game name.

This will be a step by step Guide, to set up everything - hopefully.

## Requirements
You need to have python installed on your computer.
You have to install the following modules:
- Pillow
- Requests
To install these, go to [[#Installing]]

I don't know, if the code runs on other Operating Systems than Windows, so yeah if your on Linux or Mac, Good Luck.

## Installing
- To install python you can either download it from the windows store or from the official website. Python 3.12 is recommended, since it is the version used to create this project, but it shouldn't really matter.
- To install the python modules you can run ```pip install pillow``` and ```pip install requests``` in the terminal. (To open that type cmd in the windows search (Windows key))

## Getting started
> [!CAUTION]
> NEVER GIVE AWAY YOUR STEAM API KEY TO ANYONE!

1. Download the files<br>since you only need the files in the src folder, you can delete the other files and extract all files from said folder
2. Open the user_data.py in a text or code editor
3. Fill in at least the path to steam, if you want images next to the names, you have to also insert your Steam API Key and your Steam Profile ID.<br>For further information go to [[#adding image Icons|adding image Icons]]
4. run run_Starter.bat
5. If it works, you can click on update (only, if you have entered the Steam API Key and your Steam Profile ID) and the Icons should appear (this takes a while)

- If you want to change for example the size or font of the text or the position, in which the window will appear go to user_config.py [go to Customizing for more details](#Customizing)
- You can have [different Instances](#Multiple%20Instances) of the application
  

The recommended use of the batch file is to, create a link to it (right click → create link) and then change the properties of the link, to start (run) minimized (right click → properties →  run). That way, only the python program opens, and the cmd window, which opens as well won't show up, because it is minimized and therefore only appears in the Task Bar.

## Customizing
To Configure anything you need to go to the user_config.py file

- The std means standard and is there to reset to default values if wanted
- Most of the used variable names are self-explanatory or the meaning behind them get's explained, so read those comments (anything behind a # is considered a comment)
- If you change the font size to be bigger, it might happen, that you need to increase the img_size (size of the images) as well
- You can use hex values for the colors.
- Steamworks Common Redistributables is not a game you can play, if you run it, steam will open, so it is hidden by default, but you might not have it.
- If you want to exclude certain games, insert them with apostrophes, separated with a comma in the brackets f. e. \["Game1", "Game2"]
- To only include certain games, do the same thing

## adding image Icons
 Adding your SteamAPI Key and your Profile ID is necessary because, in order to get the images the program uses the Steam API and for the API request, it needs these informations.

You can also add those image Icons manually. This is necessary for games, which you own, through the family library, because the program doesn't aquire it through the Steam API.

To add the games manually do the following:
1. create a folder named ```images``` in the same folder, as the program<br>The folder now should at least contain:
	- images
	- application.py
	- helper.py
	- user_data.py
	- user_config.py
	- main.py
	- run_starter.bat
 
 2. Navigate to your Steam installation and then to \steam\games and then there should be all of the icons.
 3. For the program to recognize the right image, you need to rename the images in the form of {appid}.jpg
 4. Save the image in the images folder 

To get the appid of a game, simply run get_appids.py

## Multiple Instances

1. create a second user config file by saving the old one under a different name (the name is irrelevant, as long, as the file has a .py extension) and then configuring it .

2. also duplicate the batch file and change the command to:
   python main.py -cfg_file {name_of_your_config_file}
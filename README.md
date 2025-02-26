# SteamGameOpener
Creates a tkinter window, in which you choose the game you want to play and then opens it.

The reason behind this project was to free Space on my Desktop while still having the img_icons next to  the game name.

This will be a step by step Guide, to set up everything - hopefully.

1. Download the files
  since you only need the files in the src folder
2. Specify the Variables in user_data.py
3. run open_application.bat

- If you want to change f. e. the size of the text or the position, in which the window will appear go to user_config.py [go to Customizing for more details](#Customizing)
- You can have [different Instances](#Multiple%20Instances) of the application

The recommended use of the batch file is to, create a link to it (right click → create link) and then change the properties of the link, to start (run) minimized (right click → properties →  run). That way, only the python program opens, and the cmd window, which opens as well won't show up, because it is minimized and therefore only appears in the Task Bar.

To Configure anything you need to go to the user_config.py file
- The std means standard and is there to reset to default values if wanted
- If you change the font size to be bigger, it might happen, that you need to increase the img_size as well
- You can use hex values for the colors.
- Steamworks Common Redistributables is not a game you can play, if you run it, steam will open, so it is hidden by default
- If you want to exclude certain games, insert them with apostrophes, separated with a comma in the brackets f. e. \["Game1", "Game2"]
- To only include certain games, do the same thing


## Multiple Instances
1. create a second user config file by saving the old one under a different name.
2. also duplicate the batch file and change the command to:
   python application.py -cfg_file {name_of_your_config_file}

# SteamGameOpener

Creates a window, in which you choose the game you want to play and then opens it.

The reason behind this project was to free space on my Desktop while still having the image icons next to the game name.

## Requirements

You need to have python installed on your computer. The requirements can be found under [requirements.txt](src\requirements.txt)
Installing via pip:

```code:
pip install -r requirements.txt
```

or:

```code:
pip install <module>
```

## Getting started

> [!CAUTION]
> NEVER GIVE AWAY YOUR STEAM API KEY TO ANYONE!

1. Download the src folder
2. Run the ``main.py`` (e.g. with ``python main.py``) and let it create the ``user_data.yaml`` and the ``config.yaml`` file
3. Try to click the Update button. If your games appear, it means you don't have to config other stuff.
4. Otherwise open the user_data.yaml file in a text or code editor and at least fill out the Steam Path variable.
5. The rest of the options will be explained under [Customizing](#customizing) and under [Multiple Instances](#multiple-instances)

## Customizing

There are 2 config files created upon start.
In the ``user_data.yaml`` file there will be all the data, every instance (see [Multiple Instances](#multiple-instances)) shares,
like your Steam API Key, your Profile ID and your setting on how to copy the game icons.

Under ``config.yaml`` you configure stuff like, where the window appears, the colors, which games appear and other stuff, which will
be explained in the comments of file itself.

For all options see [User Data](#user-data) and [User config](#user-config)

### User Data

> [!CAUTION]
> NEVER GIVE AWAY YOUR STEAM API KEY TO ANYONE!

The ``Steam API Key`` and ``Steam Profile ID`` are only needed if you want to get the icons reliably (internet connection needed)
Otherwise you can leave them at ""

 | Config Name | Explanation |
 | --- | --- |
 | Steam Path | The path to your Steam Installation. The backslashes in the Path need to be escaped, meaning, instead of ``C:\Program Files (x86)\Steam`` you need to type ``C:\\Program Files (x86)\\Steam``. This path is also the default Windows installation path. |
 | Steam API Key | Get your Steam API Key under <http://steamcommunity.com/dev/apikey> |
 | Steam Profile ID | Your Profile ID |
 | Hashes to ignore | When trying to get the images offline, some games can't be automatically identified. Then the game icons under ``Steam/steam/games`` will be copied to the created image folder. There you can manually rename the file to ``<appid>.jpg``. To get the ``appid`` you can run ``python main.py --appid`` and then click on the corresponding game. If you manually renamed the file, be sure to add the hash of the original file to the list of ``Hashes to ignore`` because then it won't be copied again. |
 | Ignore unkown Hashes | Can be used, if you don't want these hashes to be copied over |
 | Source | Sets how the app tries to fetch the game icons. Has three options: ``auto``, ``offline``, ``online``. When set to ``offline`` it only tries to identify the games under ``Steam/steam/games``, when set to ``online`` the ``Steam API Key`` and the ``Steam Profile ID`` must be set, since it needs those for the API request. When set to ``auto`` it checks if both the ``Steam API Key`` and the ``Steam Profile ID`` are given, if not it goes to ``offline``. Note that it **doesn't** switch to ``offline`` if an error occures while trying to fetch with ``online`` |

For the interested, here's how to grab the Steam Icon via Steam API:
``https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=<API_Key>&steamid=<Profile_ID>&format=json&include_played_free_games=1&include_appinfo=1&skip_unvetted_apps=false&include_free_sub``

It makes this request, goes into response, then loops through every game in games and grabs the img_icon_url.
From There it downloads the request from:
``http://media.steampowered.com/steamcommunity/public/images/apps/<appid>/<img_icon_url>.jpg``

### User Config

 | Config Name | Explanation |
 | --- | --- |
 | title | The name of the Window |
 | background | The color as a name or the rgb value of the background. |
 | foreground | The same as ``background`` |
 | Position | The starting position on screen in pixels, if ``null``, it will default to ``0``, except both ``x`` and ``y`` are ``null``, then it will automatically be centered. To start at ``0,0``, specify ``0`` |
 | Size | The height and width of the window in pixels. If both are set to ``null`` it will automatically adjust it's size. |
 | Font | Specify the font family and size. |
 | Image Size | The size of the images in pixels, when set to ``null``, the programm will decide how big it is. It assumes, the images are a square. |
 | Scrollbar color | Configure the same as ``background`` and ``forground``. Use ``solid <color>`` for the border, otherwise it won't be displayed. |
 | Sort by Appid | Sorts the games by appid instead of your custom order |
 | Sort by Cusom Order | The games appear in the order, given by ``games.txt`` (file will be created upon update button). This option overrides Sort by Appid. |
 | Games exlude | A list of all games, which should not appear in this instance. The name of the app, as in ``games.txt``, currently not the appid. |
 | Games only show | A list of all games, which should be the only games to appear in the instance. Again, only the names written in ``games.txt`` are valid. Be sure to leave it empty, if it is unwanted, since it overwrites Games exclude. |
 | Hide SteamworksCommon Redistributable | Adds the ``SteamworksCommon Redistributable`` "game" to Games exlude and thus is not shown. |

## Multiple Instances

To create different lists of games and or use different colors etc. copy your config.yaml file and rename it to whatever you like.
If you want to only change a few options from the **default** options, just keep those. Be sure to leave the structure the same.
This also works with the normal config.yaml file.
In this new file, change the configs the way you want them. The intention behind multiple instances, is so you can group games together e.g. FPS, Sudoku, RPG, Online, Indie, Soundtracks, etc.
To then start the app with that config run:

```code:
python main.py -c <Your Config>
```

## Command line Options

| Option | Explanation |
| -h --help | Shows the help message, automatically created by the argparse module |
| -c --config | Either the absolut path to the config, or the relative path to main.py |
| --copy_icons | Copys the icons, without the update button |
| --no_main | Suppresses the Main Window, intended for usage with --copy_icons |
| --appids | Prints the appids to console (stdout) and creates a GUI on which you can click to copy the AppID to your Clipboard. |

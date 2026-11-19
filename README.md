# SteamGameOpener

- [SteamGameOpener](#steamgameopener)
  - [Requirements](#requirements)
  - [Getting started](#getting-started)
  - [Customizing](#customizing)
  - [User Data](#user-data)
    - [Steam path](#steam-path)
    - [Steam API Key](#steam-api-key)
    - [Steam Profile ID](#steam-profile-id)
    - [Linux Exe Command](#linux-exe-command)
    - [Steam Games](#steam-games)
    - [Custom Games](#custom-games)
    - [Get Game Icons](#get-game-icons)
  - [User Config](#user-config)
    - [Main Window](#main-window)
    - [Scrollbar](#scrollbar)
    - [Sort By](#sort-by)
    - [Games](#games)
  - [Multiple Instances](#multiple-instances)
  - [Command line Options](#command-line-options)
  - [Manually Download Steam Icons](#manually-download-steam-icons)


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
4. Otherwise, open the user_data.yaml file in a text or code editor and at least fill out the Steam Path variable.
5. The rest of the options will be explained under [Customizing](#customizing) and under [Multiple Instances](#multiple-instances)

## Customizing

There are 2 config files created upon start.
In the ``user_data.yaml`` file there will be all the data, every instance (see [Multiple Instances](#multiple-instances)) shares,
like your Steam API Key, your Profile ID and your setting on how to copy the game icons.

Under ``config.yaml`` you configure stuff like, where the window appears, the colors, which games appear and other stuff.

All Options are more likely to be explained in the files comments, rather than this README,
but the README will be updated from time to time as well :)

For (almost) all options see [User Data](#user-data) and [User config](#user-config)

## User Data

> [!CAUTION]
> NEVER GIVE AWAY YOUR STEAM API KEY TO ANYONE!

> [!CAUTION]
> The latest version allows you to specify commands that will be executed by the application.
> Therefore, never use a user_data.yaml file from an untrusted source.
> A malicious configuration file could execute arbitrary commands, potentially installing malware or compromising your system.

The ``Steam API Key`` and ``Steam Profile ID`` are only needed if you want to get the icons reliably (internet connection needed)
Otherwise you can leave them at "".

From here on the config files will be explained with the options.

Please note, that this will not necessarily be up-to-date, so be sure to read the comments on the config files, as those will be more accurate to what you can do.

### Steam path

The path to your Steam Installation.\
The Path needs to be escaped, meaning, instead of ``C:\Program Files (x86)\Steam`` you need to type ``C:\\Program Files (x86)\\Steam``.\
This path is also the default Windows installation path.

### Steam API Key

Get your Steam API Key under <http://steamcommunity.com/dev/apikey>.\
AND NEVER SHARE IT!

### Steam Profile ID

Your Profile ID

To get your profile ID, go into Steam → Settings\
The link in the upper left corner has the form of https://steamcommunity.com/profiles/<profile ID\>/\
If you click on that link, it will copy to clipboard

### Linux Exe Command

For choosing how the .exe files are going to be opened under Linux. Default is ``wine``.

### Steam Games

This is for adding the Exe Path to your existing Steam Games, so e.g. the program doesn't recognize "Munchkin.exe" as the EXE file for the Game Munchkin Digital, so you can type:

```yaml
Steam Games:
  - Name: "Munchkin Digital"
    AppID: 1722860
    Exe Path: "Munchkin Digital/Munchkin.exe"
  - Name: "Doki Doki Literature Club"
    Exe Path: "Doki Doki Literature Club/DDLC.exe"
```

Please make sure to write "Munchkin Digital\\\\Munchkin.exe" instead of "Munchkin Digital\\Munchkin.exe", when on Windows, otherwise the program will crash.

Note that either ``Name`` or ``AppID`` must be given, not both, but both work as well :)\
Well until the name doesn't match the AppID, then you have Problems :|

### Custom Games

Similar to ``Steam Games``, but for games installed outside steam.
They can only be started via Exe, so either ``Run Command`` or ``Exe Path`` must be given.

You have the options Name, Exe Path, Run Command and AppID.\
The ``Name`` is the name. This will be displayed in the program.\
The ``AppID`` must be negative and is for identifying the image of the game, so put the games icon as a PNG, or JPEG in the /Images folder.\
The ``Exe Path`` is for starting the Game (obviously), should be absolute path.\
``Run Command`` is intended for Linux users, who can start games via flatpak, but feel free to abuse this. It basically just executes the command instead of opening the EXE file. (I think this could be used, to start Flash Games as well.)

``Run Command`` takes priority over ``Exe Path``.

So to run Prism Launcher, I use:

```yaml
Custom Games: 
  - Name: "Prism Launcher"
    Run Command: "/usr/bin/flatpak run --branch=stable --arch=x86_64 --command=prismlauncher --file-forwarding org.prismlauncher.PrismLauncher @@u %U @@"
    AppID: "-1"
```

### Get Game Icons

This has a few settings.

When trying to get the images offline, some games can't be automatically identified. Then the game icons under ``Steam/steam/games`` will be copied to the created image folder. There you can manually rename the file to <appid\>.jpg or <appid\>.png.\
Before you do that, be sure to add the hash of the original file to the list of ``Hashes to ignore`` because then it won't be copied again.\
To get the appid you can run :

```code
python main.py --appid
```

Then click on the corresponding game. This will copy the appid to your clipboard.

If you don't want that the files to be copied set the setting ``Ignore unkown Hashes`` to ``true``.

The last setting ``source`` sets how the app tries to fetch the game icons. 
\
It has three options: ``auto``, ``offline`` and ``online``.\
When set to ``offline`` it only tries to identify the games under Steam/steam/games.\
When set to ``online`` the ``Steam API Key`` and the ``Steam Profile ID`` must be set, since it needs those for the API request.\
When set to ``auto`` it checks if both the ``Steam API Key`` and the ``Steam Profile ID`` are given, if not it goes to ``offline``. Note that it **doesn't** switch to ``offline`` if an error occures while trying to fetch with ``online``.

## User Config

### Main Window

| Config Name | Explanation |
| --- | --- |
| Title | The name of the Window |
| Background | The color as a name or the RGB value of the background. |
| Foreground | The same as ``Background``, but for the ``Foreground``. |
| Position | The starting position on screen in pixels, if ``null``, it will default to ``0``, except both ``x`` and ``y`` are ``null``, then it will automatically be centered. To start at ``0,0``, specify ``0`` |
| Size | The height and width of the window in pixels. If both are set to ``null`` it will automatically adjust its size. |
| Font | Specify the font family and size. |
| Image Size | The size of the images in pixels, when set to ``null``, the program will decide how big it is. It assumes, the images are a square. BREAKS WHEN SET TO ``null``, DON'T KNOW WHY. |

### Scrollbar

| Config Name | Explanation |
| --- | --- |
| Deactivate Scrollbar | Guess what it does :) |
| Custom Scrollbar | Only if ``true`` the colors below take effect. |
| Scrollbar color | Configure the same as ``Background`` and ``Foreground``. Use ``solid <color>`` for the border, otherwise it won't be displayed. |

### Sort By

| Config Name | Explanation |
| --- | --- |
| Appid | Sorts the games by appid instead of your custom order |
| Custom Order | The games appear in the order, given by ``games.txt`` (file will be created upon update button). This option overrides Sort by Appid. |

### Games

| Config Name | Explanation |
| --- | --- |
| Exclude | A list of all games, which should not appear in this instance. The name of the app, as in ``games.txt``, or the appid. |
| Only show | A list of all games, which should be the only games to appear in the instance. Again, the names written in ``games.txt`` and the appid are both valid. Be sure to leave it empty, if it is unwanted, since it overwrites Games exclude. |
| Hide SteamworksCommon Redistributable | Adds the ``SteamworksCommon Redistributable`` "game" to Games exclude and thus is not shown. |

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
| --- | --- |
| -h --help | Shows the help message, automatically created by the argparse module |
| -c --config | Either the absolute path to the config, or the relative path to main.py |
| --copy_icons | Copies the icons, without the update button |
| --no_main | Suppresses the Main Window, intended for usage with --copy_icons |
| --appids | Prints the appids to console (stdout) and creates a GUI on which you can click to copy the AppID to your Clipboard. |

## Manually Download Steam Icons

For the interested, here's how to grab the Steam Icon via Steam API:
``https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=<API_Key>&steamid=<Profile_ID>&format=json&include_played_free_games=1&include_appinfo=1&skip_unvetted_apps=false&include_free_sub``

It makes this request, goes into response, then loops through every game in games and grabs the img_icon_url.
From There it downloads the request from:
``http://media.steampowered.com/steamcommunity/public/images/apps/<appid>/<img_icon_url>.jpg``

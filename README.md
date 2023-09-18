# WTManageSquadron
War thunder manager squadron is a simple project that has for objective to be able to manage your manager squadron with ease. After X time of a player inactivity, it will send an alert to a discord bot to warn administrator.

## What is the point of this project ? 
Follow squadron's members activity and tracks inactive members with ease


## Requirements
Only work with the english link of war thunder squadron
ex of link: 
```
https://warthunder.com/en/community/claninfo/Magnum%20Opus
https://warthunder.com/en/community/claninfo/Grief
```

Rename env_example to .env and fill variable
```
# Discord
DISCORD_WEBHOOK_URL = # This is a url to be able to send message to a bot in a discord channel, you can follow this tutorial : https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks

# Squadron
SQUADRON_URL= # This is the url link of your squadron web page
SQUAD_NAME= # Your squadron name

# DB RELATED
DB_NAME=squadron.db # A name to give to the database where all your squadron information will be stored

# Path to save file
path_to_save_html_file= # full path and must exist (don't add / at the end)
path_to_save_graph= # full path and must exist (don't add / at the end)

# LOGGING
NB_OF_LOG_FILE=3 (number of log file you want to keep)
LOGFILE_LOCATION='squadron_script.log' (ex : /tmp/wt_script.log)

# Optionnal paramaters
consecutive_day_of_inactivty = 21 # Number of consecutive day below the min_activity_required (default = 21 days)
min_activity_required = -1 # Set the minimun activity to reach before being flag as inactive (default = 0)
#nb_day_of_grace = "0"# Number of day before actually checking if the player is inactive (default = 0) (not working)
```

```
# Set up virtual env
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## How to use
/<your_to_your_venv>/venv/bin/python main.py
```
# or setup a cronjob
00 23 * * * /<your_to_your_venv>/venv/bin/python main.py
```

## How it works
Basically, you'll need to run the main.py every day.
By default, it will only send a discord message when the player is inactive for 21 consecutive days at 0 activity

You can tweak the optional vars to adapt to your own liking

Scenario example : 
You set up :  
- consecutive_day_of_inactivty = 5
- min_activity_required = 200  

We take Billy activity on the last 5 days : [360,360,360,280,150] (not flagged as inactive)  
We take John : [100,100,100,0,0] (flagged as inactive)  
But wait, what about Mac_Banana who just came in and has 0 activity: [0,100,150] (not flagged as inactive)

Note : player can gather a maximum of 360 activity point each 3 days 


### Logging system (in case of error and such)
All the logging information are in a file define by LOGFILE_LOCATION variable, that you can change. It will create a .tar file contaning the log (use 7zip to open and have a look).


## TODO
- [] : catching discord error

## Author Information
This project was created in 2023 by YohanWD
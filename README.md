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
```

## How to use
python daily.py (it is easier to set a cronjob to do the tricks every day)

## How to project Works
Bassicaly you'll need to run the daily.py every day.
For the moment, it will only send a warning when the player is inactive for 3 week (at 0 activity)


## TODO
- [] : Add a treshold to define inactive (ex : if player doesn't have 700pts send alert)
- [] : Add more option to define when a player is inactive

## Author Information
This project was created in 2023 by YohanWD
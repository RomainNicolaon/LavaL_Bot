![GitHub last commit](https://img.shields.io/github/last-commit/LavaL18/Algosup-Discord)

## LavaL_Bot 
*(forked from [Algobot](https://github.com/PaulMarisOUMary/Algosup-Discord))*

## Setting up the bot

<details>
  <summary>Get started</summary>
  
  - Paste your token  BOT in `auth/token.dat`.
  - Please make sure you have activated the `Privileged Gateway Intents` in [Discord Developpers](https://discord.com/developers/applications) for your application.
	  - [x] PRESENCE INTENT
	  - [x] SERVER MEMBERS INTENT
  - Install with `pip` all dependencies :
	  - [x] `python3 -m pip install -U discord.py`
	  - [x] `python3 -m pip install -U DateTime`
	  - [x] `python3 -m pip install -U matplotlib`
	  - [x] `python3 -m pip install -U O365`
	  - [x] `python3 -m pip install -U Pillow`
	  - [x] `python3 -m pip install -U googletrans==4.0.0-rc1`
	  - [x] `python3 -m pip install -U youtube_dl`
	  - [x] `python3 -m pip install -U PIL`
  - Edit line `12` on `bot.py` to change the bot prefix : `command_prefix=commands.when_mentioned_or("PREFIX_HERE")`.
  - If you want to use admin commands edit the line `7` on `cogs/admin.py`and paste your user ID (more informations [here](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-))
</details>

## Contributors

[![contributors](https://github.com/LavaL18/LavaL_Bot/graphs/contributors)



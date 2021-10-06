![GitHub is maintained](https://img.shields.io/maintenance/yes/2022?color=success)
![GitHub last commit](https://img.shields.io/github/last-commit/LavaL18/LavaL_Bot)
.. image:: https://img.shields.io/pypi/v/discord.py.svg
   :target: https://pypi.python.org/pypi/discord.py
   :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/discord.py.svg
   :target: https://pypi.python.org/pypi/discord.py
   :alt: PyPI supported Python versions

## LavaL_Bot 
*(forked from [Algobot](https://github.com/PaulMarisOUMary/Algosup-Discord))*

## Getting started

### Prerequisites

Install few packages with pip and the v 2.0.0a of discord.py
- pip 
```bash
$ python3 -m pip install -U matplotlib
$ python3 -m pip install -U O365
$ python3 -m pip install -U Pillow
$ python3 -m pip install -U googletrans==4.0.0-rc1
$ python3 -m pip install -U tzlocal==2.1
```
- git
```bash
$ git clone https://github.com/Rapptz/discord.py
$ cd discord.py
$ python3 -m pip install -U .[voice]
```

### Installation
1. Create a application on  [Discord Developpers](https://discord.com/developers/applications)

2. Enable the bot status in  [Discord Developpers/applications/bot](https://discord.com/developers/applications/YOUR_APP_ID/bot)

3. Please make sure you have activated each `Privileged Gateway Intents` in [Discord Developpers/applications/bot](https://discord.com/developers/applications) for your application.

4. Paste your BOT token in `auth/token.dat`.

5. (Optional) Edit line `10` in `bot.py` to change the bot prefix : `command_prefix=commands.when_mentioned_or("`*PREFIX_HERE*`")`.

## Contributors

[![contributors](https://contrib.rocks/image?repo=LavaL18/LavaL_Bot)](https://github.com/LavaL18/LavaL_Bot/graphs/contributors)


## Authors

1. [@LavaL_18](https://github.com/LavaL_19) Creator of [LavaL Bot](https://github.com/LavaL18/LavaL_Bot)
2. [@Paul Maris](https://github.com/PaulMarisOUMary) LavaL Bot is a fork of [Algosup-Discord](https://github.com/PaulMarisOUMary/Algosup-Discord)'s template

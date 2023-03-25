# Igris - A Python Discord Bot

<p align="center">
  <a href="https://github.com/SlyPredator/IgrisDiscordBot/commits/main"><img src="https://img.shields.io/github/last-commit/SlyPredator/IgrisDiscordBot"></a>
  <a href="https://github.com/SlyPredator/IgrisDiscordBot/blob/main/LICENSE.md"><img src="https://img.shields.io/github/license/SlyPredator/IgrisDiscordBot""></a>
  <a href="https://github.com/SlyPredator/IgrisDiscordBot"><img src="https://img.shields.io/github/languages/code-size/SlyPredator/IgrisDiscordBot"></a>
  <a href="https://github.com/SlyPredator/IgrisDiscordBot/issues"><img src="https://img.shields.io/github/issues-raw/SlyPredator/IgrisDiscordBot"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
  <a href="https://conventionalcommits.org/en/v1.0.0/"><img src="https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white"></a>
</p>

# Igris 
A Discord bot for my private server.

## Support

Before requesting support, you should know that this requires you to have at least a **basic knowledge** of
Python and the library is made for advanced users. Do not use this if you don't know the
basics. [Here's](https://pythondiscord.com/pages/resources) a link for resources to learn python.

If you need some help for something, do not hesitate to join the Discord server for discord.py [here](https://discord.com/invite/dpy).

## Disclaimer

Slash commands can take some time to get registered globally, so if you want to test a command you should use
the `@app_commands.guilds()` decorator so that it gets registered instantly. Example:

```py
@commands.hybrid_command(
  name="command",
  description="Command description",
)
@app_commands.guilds(discord.Object(id=GUILD_ID)) # Place your guild ID here
```


## How to download it

* Clone/Download the repository
    * To clone it and get the updates you can definitely use the command
      `git clone`
* Create a discord bot [here](https://discord.com/developers/applications)
* Get your bot token
* Invite your bot on servers using the following invite:
  https://discord.com/oauth2/authorize?&client_id=YOUR_APPLICATION_ID_HERE&scope=bot+applications.commands&permissions=PERMISSIONS (
  Replace `YOUR_APPLICATION_ID_HERE` with the application ID and replace `PERMISSIONS` with the required permissions
  your bot needs that it can be get at the bottom of a this
  page https://discord.com/developers/applications/YOUR_APPLICATION_ID_HERE/bot)

## How to set up

To set up the bot there is now a [config.json](config.json) file where you can put the
needed things to edit.

Here is an explanation of what everything is:

```json
{
  "prefix": # The prefix for the bot,
  "permissions": # The permissions integer from the Discord Developer tab for your bot,
  "bot_token": # The token for your bot,
  "bot_application_id": # The application ID of your bot,
  "sync_commands_globally": true,
  "owners": [],
  "moderators": []
}
```

There's also a `.env` file required, with the following keys:

```
BOT_TOKEN="Your Bot Token from Discord Developer Portal"
RS_API_TOKEN="Random Stuff API Key"
RAPIDAPI_TOKEN="RapidAPI Key"
```

## How to start

To start the bot you simply need to launch, either your terminal (Linux, Mac & Windows), or your Command Prompt (
Windows)
.

Before running the bot you will need to install all the requirements with this command:

```
python -m pip install -r requirements.txt
```

After that you can start it with

```
python bot.py
```

> **Note** You may need to replace `python` with `py`, `python3`, `python3.11`, etc. depending on what Python versions you have installed on the machine.
## Built With

* [Python 3.11.0](https://www.python.org/)

## License

This repository is based off of a template [from kkrypt0nn](https://github.com/kkrypt0nn/Python-Discord-Bot-Template).

See [the license file](https://github.com/kkrypt0nn/Python-Discord-Bot-Template/blob/master/LICENSE.md) for more
information.

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details.

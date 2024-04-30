# YTDL - YouTube Downloader

Telegram bot based on Aiogram, Pyrogram and PyTube that allows to download any kind of videos from YouTube.
Bot requires extra telegram account for bypassing file limits for bots and one Google account for accessing YouTube.

<div align="center">
<img alt="YouTube" src="https://img.shields.io/badge/YouTube-red?style=for-the-badge&logo=youtube&logoColor=white"/>
<img alt="Telegram" src="https://img.shields.io/badge/Telegram-blue?&style=for-the-badge&logoColor=white&logo=telegram"/>
<img alt="Python" src="https://img.shields.io/badge/python-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/>
<img alt="SQLite" src="https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white"/>
</div>

## Creating Database

You do not have to create it manually. It is formed automatically.

## Configuring Environments
- `ADMIN_ID` : Your account`s Telegram ID.
- `TOKEN`: Bot`s token, can be obtained here - https://t.me/BotFather.
- `BOT_ID`: Bot`s Telegram ID.
- `HOST_ID`: Telegram ID of an account that will be used to bypass 2 gb file restriction.
- `API_ID`: Can be obtained here - https://my.telegram.org.
- `API_HASH`: Can be obtained here - https://my.telegram.org.

**There you can find an example of .env file.**

## Connecting Google account
#### First time you launch account.py you have to follow the link shown in terminal and enter the code that will also be displayed in terminal.
#### This will allow the bot to use your Google account in order to get access to YouTube.

### Show some ❤️ and ⭐ the repo to support the project!
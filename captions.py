from aiogram.utils.markdown import hlink, hbold

VIDEO_CAPTION: str = f'''
{hbold('✅ Скачано с помощью ')}{hlink(title='YTDL | Скачать с Youtube/Youtube Shorts',
                                      url='https://t.me/yt_shorts_download_bot')}
💚 Спасибо за использование нашего бота!'''

START_MESSAGE: str = f"""👋 {hbold('Вас приветствует бот для загрузки видео.')}
\nИмеется возможность загрузки из следующих источников:
❤ {hbold('YouTube')}
❤ {hbold('YouTube Shorts')}"""

LINK_NOT_FOUND: str = f'''✋ {hbold("Упс, ссылка не найдена.")}'''

MULTIPLE_LINKS: str = f'''🛑 {hbold("Пожалуйста. отправьте ссылку только на одно видео.")}'''

DOWNLOADING_STARTED: str = f'''✔ {hbold("Отлично, загрузка видео началась.")}'''

WAIT: str = f"""🛑 {hbold('Пожалуйста, дождитесь пока загрузится предыдущее видео.')}"""

DOWNLOAD_FAILED: str = f'''✋ {hbold("Не удалось скачать видео. Попробуйте позже.")}'''

VIDEO_UNAVAILABLE: str = f'''✋ {hbold("Видео недоступно или ограничено.")}'''

FILE_TOO_BIG: str = f'''🛑 {hbold("Видео слишком большое для отправки.")}'''

SEND_FAILED: str = f'''✋ {hbold("Видео скачалось, но не удалось его отправить. Попробуйте позже.")}'''

# Operational alert relayed by the userbot worker to the admin. Plain text,
# no markup: it travels host -> bot -> admin and is forwarded verbatim.
COOKIES_EXPIRED: str = (
    '⚠️ YouTube требует вход — cookies устарели.\n'
    'Загрузки не работают, пока не обновишь data/cookies.txt на сервере.'
)

import re
from typing import Union, Dict, List

from aiogram import types
from aiogram.filters import BaseFilter


class IsCorrectLink(BaseFilter):
    """
    Checks if the YouTube link is correct.

    On a match it returns a dict; aiogram 3 merges that into the handler's
    keyword arguments, so the matched IDs arrive as the ``matches`` parameter.
    """

    async def __call__(self, message: types.Message) -> Union[bool, Dict[str, List[str]]]:
        # aiogram 3 runs every handler's filters on every message; a video or
        # other non-text message has `text=None`, which would crash re.findall.
        if not message.text:
            return False

        pattern1: str = r'(?:https?://)?(?:www\.)?youtube\.com/shorts/([\w\-]+)'
        pattern1_matches: List[str] = re.findall(pattern1, message.text)

        pattern2: str = r'(?:youtu\.be/|youtube\.com/watch\?v=)([\w\-]+)'
        pattern2_matches: List[str] = re.findall(pattern2, message.text)

        matches: List[str] = pattern1_matches + pattern2_matches
        if len(matches) == 0:
            return False
        else:
            return {'matches': matches}

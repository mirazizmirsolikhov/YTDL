import re
from typing import Union, Dict, List

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsCorrectLink(BoundFilter):
    """
    Checks if the YouTube link is correct.
    """
    key: str = 'is_correct_link'

    async def check(self, message: types.Message) -> Union[bool, Dict[str, List[str]]]:
        pattern: str = (r'^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(?:-nocookie)?\.com|youtu.be))(\/(?:['
                        r'\w\-]+\?v=|embed\/|live\/|v\/|shorts\/)?)([\w\-]+)(\S+)?$')
        pattern_match: str = re.match(pattern, message.text).group(5)
        if len(pattern_match) == 11:
            return {'matches': [pattern_match]}
        return False

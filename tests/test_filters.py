from types import SimpleNamespace

from bot.filters.link import IsCorrectLink


async def _check(text: str):
    """Run the link filter against a message carrying the given text."""

    return await IsCorrectLink()(SimpleNamespace(text=text))


async def test_plain_watch_url():
    result = await _check('see https://www.youtube.com/watch?v=dQw4w9WgXcQ here')
    assert result == {'matches': ['dQw4w9WgXcQ']}


async def test_short_youtu_be_url():
    result = await _check('https://youtu.be/dQw4w9WgXcQ')
    assert result == {'matches': ['dQw4w9WgXcQ']}


async def test_shorts_url():
    result = await _check('https://youtube.com/shorts/abc123DEF45')
    assert result == {'matches': ['abc123DEF45']}


async def test_text_without_link():
    assert await _check('just a plain message') is False


async def test_message_without_text():
    """A non-text message (e.g. a video) has text=None and must not crash."""

    assert await _check(None) is False


async def test_multiple_links_are_all_matched():
    result = await _check(
        'https://youtu.be/aaaaaaaaaaa then https://youtu.be/bbbbbbbbbbb'
    )
    assert result == {'matches': ['aaaaaaaaaaa', 'bbbbbbbbbbb']}

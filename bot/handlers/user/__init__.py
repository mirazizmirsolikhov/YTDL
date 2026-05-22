from .start import dp
from .video_url import dp
from .fallback import dp  # registered last: catches messages no handler claimed

__all__ = ['dp']

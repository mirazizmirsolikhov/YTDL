from .is_admin import IsAdmin
from .is_host import IsHost
from .link import IsCorrectLink

# aiogram 3 has no filters factory — filters are passed straight to the
# handler decorators, so these classes only need to be importable.
__all__ = ['IsAdmin', 'IsHost', 'IsCorrectLink']

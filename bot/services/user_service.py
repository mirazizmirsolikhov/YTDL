from aiogram import types

from loader import db


def register_or_update(user: types.User) -> None:
    """Ensure the user exists in the database and refresh their profile data.

    Creating the user when missing and then updating keeps the row in sync on
    every interaction, not just on /start.
    """

    if not db.user_exists(user.id):
        db.create_user(user_id=user.id, first_name=user.first_name, username=user.username)
    db.update_user(user_id=user.id, first_name=user.first_name, username=user.username, is_active=1)

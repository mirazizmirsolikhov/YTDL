import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()

ADMIN_ID = os.getenv('ADMIN_ID')


def create_database() -> None:
    """
    Creates the database with all required tables.
    """
    database = sqlite3.connect("users.db")
    cursor = database.cursor()

    cursor.executescript(
        '''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            first_name VARCHAR(64) NOT NULL,
            username VARCHAR(32) UNIQUE,
            status BOOL NOT NULL,
            is_superuser BOOL NOT NULL,
            is_active BOOL,
            number_of_downloads INTEGER DEFAULT (0)
        );
        '''
    )
    cursor.executescript(
        '''
        CREATE TABLE IF NOT EXISTS links(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id VARCHAR NOT NULL,
            url VARCHAR(11) NOT NULL
        );
        '''
    )
    cursor.execute(
        '''
        INSERT INTO users (user_id, first_name, status, is_superuser, is_active)
        VALUES (?, ?, ?, ?, ?);
        ''',
        (ADMIN_ID, 'admin', 0, 1, 1))
    database.commit()
    database.close()


create_database()

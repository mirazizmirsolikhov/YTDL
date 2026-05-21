import os

# Dummy settings so `config` can be instantiated during test collection,
# before any project module that imports it is loaded. Real values are never
# needed: the tests exercise pure logic, not Telegram or a live Redis.
os.environ.setdefault('ADMIN_ID', '1')
os.environ.setdefault('TOKEN', '123456:test')
os.environ.setdefault('BOT_ID', '2')
os.environ.setdefault('HOST_ID', '3')
os.environ.setdefault('API_ID', '4')
os.environ.setdefault('API_HASH', 'test')

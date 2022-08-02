import os.path


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


# Google API
CREDENTIALS_FILE_NAME = ''
CREDENTIALS_FILE_PATH = os.path.join(ROOT_DIR, CREDENTIALS_FILE_NAME)
SPREADSHEET_ID = '1BkcYdJamiszwryvC_tPxWOesEXu_ieooWoFheiVDp6A'


# PostgreSQL
PG_USER = 'postgres'
DB_NAME = 'test_task'
PG_PASSWORD = '123456'
PG_HOST = '127.0.0.1'
PG_PORT = 5432

# sheetparser
PARSING_RANGE = 20
SHEET_MONITORING_DELAY = 30

# notifications
DELIVERY_MONITORING_DELAY = 60

# Telegram bot
TELEGRAM_API_TOKEN = ''

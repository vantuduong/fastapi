import os
from dotenv import load_dotenv

load_dotenv()

def get_connection_string():
    engine = os.environ.get("DB_ENGINE")
    driver = os.environ.get("DB_DRIVER")
    dbhost = os.environ.get("DB_HOST")
    username = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    dbname = os.environ.get("DB_NAME")
    return f"{engine}+{driver}://{username}:{password}@{dbhost}/{dbname}"


SQLALCHEMY_DATABASE_URL = get_connection_string()
ADMIN_DEFAULT_PASSWORD = os.environ.get("DEFAULT_PASSWORD")

JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")

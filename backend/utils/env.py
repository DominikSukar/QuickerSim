import os
from dotenv import load_dotenv

load_dotenv()


def get_var(var_name: str) -> str:
    """Get an environment variable"""
    return os.environ.get(var_name)


DATABASE_LOGIN = get_var("DB_USER")
DATABASE_PASSWORD = get_var("DB_PASSWORD")

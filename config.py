from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Setting(BaseSettings):

    db_url: str = f"postgresql+asyncpg://alik:alik2006@localhost:5432/new_people_db"
    db_echo: bool = False
    # db_echo: bool = True


settings = Setting()
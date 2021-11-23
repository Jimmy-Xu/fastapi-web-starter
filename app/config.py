import pathlib
import os
from pydantic import BaseSettings

root = pathlib.Path(__file__).parent.parent
# This will always give the correct path as long as .env is in the parent directory
env_file = os.path.join(root, '.env')


class Settings(BaseSettings):

    project_root: pathlib.Path = root
    secret: str
    db_uri: str = "sqlite+pysqlite:///app.db"
    token_url: str = "/auth/login"

    # binance
    baseUrl: str
    apiKey: str
    apiSecretKey_test: str
    baseUrl_test: str
    apiSecretKey: str
    apiKey_test: str

    ctrKey: str

    class Config:
        env_file = '.env'


print("env_file: {0}".format(env_file))

Config = Settings(_env_file=env_file)

from starlette.config import Config

config = Config()

DATABASE_URL = config('DATABASE_URL')

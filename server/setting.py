import os
from typing import List
from pydantic import BaseSettings
from dotenv import dotenv_values

dotenv_config = dotenv_values('.env')


class Settings(BaseSettings):
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    LOG_PATH = os.path.join(BASEDIR, 'logs')
    BACKEND_CORS_ORIGINS: List = ['*']

    # 默认管理员账号密码等信息
    ADMIN_USERNAME = dotenv_config.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = dotenv_config.get('ADMIN_PASSWORD', '123456')
    ADMIN_EMAIL = dotenv_config.get('ADMIN_EMAIL', 'markchen@amwisedx.com')
    ADMIN_ROLE = dotenv_config.get('ADMIN_ROLE', 'admin')

    # 数据库账号密码
    DB_HOST = dotenv_config.get('DB_HOST', '127.0.0.1')
    DB_PORT = dotenv_config.get('DB_PORT', 5432)
    DB_USER = dotenv_config.get('DB_USER', 'mark')
    DB_PASSWORD = dotenv_config.get('DB_PASSWORD', 'mark123')
    DB_NAME = dotenv_config.get('DB_NAME', 'test')

    DATABASE_URI = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}'
    SQLALCHEMY_DATABASE_URI: str = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


settings = Settings()

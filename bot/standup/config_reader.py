from pydantic import BaseSettings, SecretStr
from standup.config import DEBUG_CONFIG_DIR, PRODUCTION_CONFIG_DIR
from pathlib import Path


class DebugSettings(BaseSettings):
    bot_token: SecretStr
    admin_id: SecretStr
    white_list: list

    class Config:
        env_file = DEBUG_CONFIG_DIR
        env_file_encoding = 'utf-8'
        
class ProductionSettings(BaseSettings):
    bot_token: SecretStr
    admin_id: SecretStr
    white_list: list

    class Config:
        env_file = PRODUCTION_CONFIG_DIR
        env_file_encoding = 'utf-8'


debug_config = DebugSettings()
production_config = ProductionSettings()

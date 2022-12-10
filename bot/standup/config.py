from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIGS_DIR = Path(__file__).resolve().parent

DEBUG_CONFIG_DIR = CONFIGS_DIR / 'bot_debug_config.env'
PRODUCTION_CONFIG_DIR = CONFIGS_DIR / 'bot_production_config.env'



DEBUG = False
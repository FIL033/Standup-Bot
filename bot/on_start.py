from utils.db import create_table, check_table
from standup.config import DEBUG

if DEBUG:
    import standup.debug_config as BotConfig
else:
    import standup.production_config as BotConfig

for (key, value) in BotConfig.DB_TABLES.items():
    if not check_table(key):
        create_table(name = key, columns = value['columns'])

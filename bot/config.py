from environs import Env

env = Env()
env.read_env()

# BOT_TOKEN = env.str("BOT_TOKEN", "PLACEHOLDER_TOKEN")
# ADMIN_ID = env.int("ADMIN_ID", 0)
# CHANNEL_ID = env.str("CHANNEL_ID", "PLACEHOLDER_CHANNEL") # Private channel ID
# BASE_URL = env.str("BASE_URL", "http://127.0.0.1:8000/api/")

BOT_TOKEN=env.str("BOT_TOKEN", "8523361218:AAEi_-Eu3gibXFfLqbMJ2ChSVLlbejyjpNo")
ADMINS = env.list("ADMINS", [8383818551, 2038934476])
BACKEND_URL = env.str("BACKEND_URL", "http://127.0.0.1:8000")
BOT_ID = env.int("BOT_ID", 8523361218)
DB_TG_CHANNEL = env.int("DB_TG_CHANNEL", -1003620326259)
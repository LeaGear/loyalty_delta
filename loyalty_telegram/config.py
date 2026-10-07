import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

BACKEND_POINT = "/telegram"

API_REQUESTS = {
    "test" : BACKEND_POINT + "/test/",
    "user_reg" : BACKEND_POINT + "/registration/",
    "user_status" : BACKEND_POINT + "/client_status/{}",
    "get_user_code" : BACKEND_POINT + "/loyalty_code/{}",
    "user_data" : BACKEND_POINT + "/user_data/{}",
}
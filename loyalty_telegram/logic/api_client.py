import httpx

from config import BOT_API_KEY, BACKEND_URL, API_REQUESTS

from logic.decorators import server_down

client = httpx.AsyncClient(
    base_url=BACKEND_URL,
    headers={'X-API-KEY': BOT_API_KEY},
    timeout=10
)
@server_down
async def registration_new_client(name, phone_number, user_id):
    payload = {
        'user_name' : name,
        'phone_number' : phone_number,
        'telegram_id' : user_id
    }
    return await client.post(f"{API_REQUESTS['user_reg']}", json=payload)

@server_down
async def check_user_status(user_id):
    return await client.get(f"{API_REQUESTS['user_status'].format(user_id)}")


@server_down
async def get_user_loyalty_code(user_id):
    response = await client.get(f"{API_REQUESTS['get_user_code'].format(user_id)}")
    if response.status_code == 200:
        return response.json().get('data')
    else:
        return None

@server_down
async def get_user_data(user_id):
    response = await client.get(f"{API_REQUESTS['user_data'].format(user_id)}")
    if response.status_code == 200:
        return response.json().get('data')
    else:
        return None
import httpx

from config import SERVER_API_KEY, BACKEND_URL, API_REQUESTS

from logic.decorators import server_down

@server_down
async def registration_new_client(name, phone_number, user_id):
    payload = {
        'user_name' : name,
        'phone_number' : phone_number,
        'telegram_id' : user_id
    }
    async with httpx.AsyncClient(headers={'X-API-KEY': SERVER_API_KEY}) as client:
        response = await client.post(f"{BACKEND_URL}{API_REQUESTS['user_reg']}", json=payload)
        return response

@server_down
async def check_user_status(user_id):
    async with httpx.AsyncClient(headers={'X-API-KEY': SERVER_API_KEY}) as client:
        response = await client.get(f"{BACKEND_URL}{API_REQUESTS['user_status'].format(user_id)}")
        return response

@server_down
async def get_user_loyalty_code(user_id):
    async with httpx.AsyncClient(headers={'X-API-KEY': SERVER_API_KEY}) as client:
        response = await client.get(f"{BACKEND_URL}{API_REQUESTS['get_user_code'].format(user_id)}")
        if response.status_code == 200:
            return response.json().get('data')
        else:
            return None

@server_down
async def get_user_data(user_id):
    async with httpx.AsyncClient(headers={'X-API-KEY': SERVER_API_KEY}) as client:
        response = await client.get(f"{BACKEND_URL}{API_REQUESTS['user_data'].format(user_id)}")
        if response.status_code == 200:
            return response.json().get('data')
        else:
            return None
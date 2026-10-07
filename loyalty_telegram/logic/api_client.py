import httpx

from config import BACKEND_URL, API_REQUESTS

async def fast_test():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_URL}{API_REQUESTS['test']}")
        return response.json()

async def registration_new_client(name, phone_number, user_id):
    payload = {
        'user_name' : name,
        'phone_number' : phone_number,
        'telegram_id' : user_id
    }
    print(payload)
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BACKEND_URL}{API_REQUESTS['user_reg']}", json=payload)
        return response

async def check_user_status(user_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_URL}{API_REQUESTS['user_status'].format(user_id)}")
        return response

async def get_user_loyalty_code(user_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_URL}{API_REQUESTS['get_user_code'].format(user_id)}")
        if response.status_code == 200:
            return response.json().get('data')
        else:
            return None

async def get_user_data(user_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_URL}{API_REQUESTS['user_data'].format(user_id)}")
        if response.status_code == 200:
            return response.json().get('data')
        else:
            return None
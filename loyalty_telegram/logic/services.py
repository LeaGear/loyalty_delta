

from logic.api_client import get_user_data

async def get_user_info(user_id):
    actual_data = await get_user_data(user_id)
    if actual_data is None:
        return "Something went wrong!"
    else:
        message = (f"Client: {actual_data.get('name')}\n"
                   f"\n"
                   f"Total spent: {actual_data.get('total_spent')}\n"
                   f"Discount Value --> {actual_data.get('discount_value') if actual_data.get('discount_value') else 0}%\n"
                   f"\n"
                   f"Last operation: {actual_data.get('last_operation') if actual_data.get('last_operation') else 'Not found'}\n")
        return message
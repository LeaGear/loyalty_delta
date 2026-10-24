from datetime import datetime
from logic.api_client import get_user_data

async def get_user_info(user_id):
    actual_data = await get_user_data(user_id)
    print(f"actual data -----> {actual_data}")
    if actual_data is None:
        return "Something went wrong!"
    else:

        date_str = actual_data.get("last_operation_date", "")

        print(date_str)
        if date_str:
            parsed_date = datetime.fromisoformat(date_str)
            date = datetime.strftime(parsed_date, "%Y-%m-%d %H:%M:%S")
        else:
            date = "not found"
        message = (f"Client: {actual_data.get('name')}\n"
                   f"\n"
                   f"Total spent: {actual_data.get('total_spent')}\n"
                   f"Your Tier ->> {actual_data.get('discount_level')}\n"
                   f"Discount Value --> {0 if actual_data.get('discount') is None else actual_data.get('discount') }%\n"
                   f"\n"
                   f"Last operation: {date}\n")
        return message
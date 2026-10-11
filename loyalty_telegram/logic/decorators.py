import httpx

from functools import wraps

class ResponseMock:
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        self.data = None

    def __str__(self):
        return f"<Response [{self.status_code} {self.detail}]>"

def server_down(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except httpx.ConnectError:
            return ResponseMock(status_code=503, detail='Connection error')
        except httpx.TimeoutException:
            return ResponseMock(status_code=522, detail='Timeout Exception')
    return wrapper


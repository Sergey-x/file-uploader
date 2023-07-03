import fastapi as fa
import httpx
import orjson

from file_uploader.settings import SETTINGS


async def change_user_avatar(user_id: int, avatar_filename: str) -> bool:
    """Изменение имени файла аватара пользователя на сервисе пользователя."""
    try:
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.put(
                url=f'http://{SETTINGS.SCHEDULE_SERVICE_HOSTS}/schedule/user',
                data=orjson.dumps({"userId": user_id, "avatar": avatar_filename}),  # type: ignore
                headers={'Content-Type': 'application/json'},
            )
    except httpx.ConnectError:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Connection error! Something went wrong, try later',
        )
    except httpx.ConnectTimeout:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Timeout! Something went wrong, try later',
        )

    is_avatar_created: bool = (200 <= response.status_code < 300)
    return is_avatar_created

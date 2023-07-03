import fastapi as fa
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from file_uploader.api.deps import get_db
from file_uploader.crud import FilesCRUD
from file_uploader.enums import FileOwnerTypes
from file_uploader.services import change_user_avatar

api_router = fa.APIRouter()


@api_router.delete(
    "/{file_id}",
    response_class=ORJSONResponse,
    response_model=None,
    status_code=fa.status.HTTP_204_NO_CONTENT,
    responses={
        fa.status.HTTP_204_NO_CONTENT: {
            "description": "Deleted",
        },
        fa.status.HTTP_401_UNAUTHORIZED: {
            "description": "Запрос не авторизован",
        },
    },
)
async def delete_event_file(
        file_id: int = fa.Path,
        db: AsyncSession = fa.Depends(get_db),
):
    """
    """
    await FilesCRUD.delete_event_file(db, file_id)


@api_router.delete(
    "/{owner_type}/{owner_id}",
    response_class=ORJSONResponse,
    response_model=None,
    status_code=fa.status.HTTP_204_NO_CONTENT,
    responses={
        fa.status.HTTP_204_NO_CONTENT: {
            "description": "Deleted",
        },
        fa.status.HTTP_401_UNAUTHORIZED: {
            "description": "Запрос не авторизован",
        },
    },
)
async def delete_event_files(
        owner_type: FileOwnerTypes = fa.Path,
        owner_id: int = fa.Path,
        db: AsyncSession = fa.Depends(get_db),
):
    """
    """
    await FilesCRUD.delete_event_files(db, owner_type=owner_type, owner_id=owner_id)
    if owner_type == FileOwnerTypes.USER:
        is_avatar_deleted: bool = await change_user_avatar(owner_id, "")
        if is_avatar_deleted:
            await db.commit()
        else:
            raise fa.HTTPException(status_code=fa.status.HTTP_503_SERVICE_UNAVAILABLE,
                                   detail="Удаленный сервис недоступен. Попробуйте удалить позже.")
    else:
        await db.commit()

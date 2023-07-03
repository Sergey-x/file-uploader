import fastapi as fa
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from file_uploader.api.deps import get_db
from file_uploader.crud.files import FilesCRUD
from file_uploader.enums import FileOwnerTypes
from file_uploader.schemas.upload_responses import (GetEventFilesResponse,
                                                    GetFileResponse,
                                                    LoadFileResponseItem)
from file_uploader.utils import row2dict

api_router = fa.APIRouter()

DEFAULT_AVATAR: LoadFileResponseItem = LoadFileResponseItem(id=0,
                                                            filename=None,
                                                            owner_id=0,
                                                            content_type="",
                                                            dt_created="",
                                                            size=0, )


@api_router.get(
    "/{owner_type}/{owner_id}",
    response_class=ORJSONResponse,
    response_model=GetEventFilesResponse,
    status_code=fa.status.HTTP_200_OK,
    responses={
        fa.status.HTTP_200_OK: {
            "description": "Ok",
        },
        fa.status.HTTP_401_UNAUTHORIZED: {
            "description": "Запрос не авторизован",
        },
    },
)
async def get_event_files(
        owner_type: FileOwnerTypes = fa.Path,
        owner_id: int = fa.Path,
        db: AsyncSession = fa.Depends(get_db),
) -> GetEventFilesResponse:
    """
    """
    event_files: list = await FilesCRUD.get_event_files(db, owner_id=owner_id, owner_type=owner_type)
    if len(event_files) == 0 and owner_type == FileOwnerTypes.USER:
        return GetEventFilesResponse(
            files=[DEFAULT_AVATAR],
        )

    res: GetEventFilesResponse = GetEventFilesResponse(
        files=[row2dict(f) for f in event_files],
    )
    return res


@api_router.get(
    "/{file_id}",
    response_class=ORJSONResponse,
    response_model=GetFileResponse,
    status_code=fa.status.HTTP_200_OK,
    responses={
        fa.status.HTTP_200_OK: {
            "description": "Ok",
        },
        fa.status.HTTP_404_NOT_FOUND: {
            "description": "Ресурс не найден",
        },
        fa.status.HTTP_401_UNAUTHORIZED: {
            "description": "Запрос не авторизован",
        },
    },
)
async def get_event_file(
        file_id: int = fa.Path,
        db: AsyncSession = fa.Depends(get_db),
) -> GetFileResponse:
    """
    """
    event_file = await FilesCRUD.get_event_file(db, file_id=file_id)
    if event_file is None:
        raise fa.HTTPException(status_code=fa.status.HTTP_404_NOT_FOUND, detail="Файла с указанным id не найдено.")
    res = GetFileResponse(file=row2dict(event_file))
    return res

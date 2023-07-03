from collections import defaultdict

import fastapi as fa
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from file_uploader.api.deps import get_db
from file_uploader.crud import FilesCRUD
from file_uploader.enums import FileOwnerTypes
from file_uploader.logging import get_logger
from file_uploader.utils import row2dict

logger = get_logger(__name__)

api_router = fa.APIRouter()

example_response: dict = {
    "1": [
        {
            "id": "1",
            "dt_created": "2023-04-17 15:11:21.144254+00:00",
            "dt_updated": "None",
            "is_available": "True",
            "filename": "filename.png",
            "size": "133626",
            "owner_id": "1",
            "owner_type": "FileOwnerTypes.EVENT",
            "content_type": "image/png"
        },
        {
            "id": "2",
            "dt_created": "2023-04-17 15:21:29.623552+00:00",
            "dt_updated": "None",
            "is_available": "True",
            "filename": "filename.pdf",
            "size": "185487",
            "owner_id": "1",
            "owner_type": "FileOwnerTypes.EVENT",
            "content_type": "application/pdf"
        }
    ]
}


@api_router.get(
    "/event-files-by-id",
    response_class=ORJSONResponse,
    status_code=fa.status.HTTP_200_OK,
    responses={
        fa.status.HTTP_200_OK: {
            "description": "Ok",
            "content": {
                "application/json": {
                    "example": example_response
                }
            },
        },
        fa.status.HTTP_400_BAD_REQUEST: {
            "description": "Некорректный формат входных данных",
        },
        fa.status.HTTP_401_UNAUTHORIZED: {
            "description": "Запрос не авторизован",
        },
    },
)
async def get_files_by_event_ids(
        owner_type: FileOwnerTypes = fa.Query(),
        ids: str = fa.Query(default=""),
        db: AsyncSession = fa.Depends(get_db),
):
    # проверяем, что строка формата '%d,%d,%d'
    try:
        list_id = []
        if ids:
            list_id = list(map(int, ids.split(',')))
    except TypeError:
        raise fa.HTTPException(status_code=fa.status.HTTP_400_BAD_REQUEST, detail=f"TypeError. Wrong list id {ids}.")
    except ValueError:
        raise fa.HTTPException(status_code=fa.status.HTTP_400_BAD_REQUEST, detail=f"ValueError. Wrong list id {ids}.")

    files: list = await FilesCRUD.get_events_files(db=db, owner_type=owner_type, owner_ids=list_id)

    event_files_dict: dict = defaultdict(list)

    # Заполняем пустыми значениями, даже если файлов нет - будет возвращен пустой список
    for owner_id in list_id:
        event_files_dict[str(owner_id)] = []

    # Раскидываем файлы по соответствующим обладателю словарям
    for _file in files:
        file: dict = row2dict(_file)
        event_files_dict[file.get('owner_id')].append(file)
    return event_files_dict

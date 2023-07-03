import fastapi as fa
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from file_uploader.api.deps import get_db
from file_uploader.crud import FilesCRUD
from file_uploader.enums import FileOwnerTypes
from file_uploader.schemas import UploadFileResponse
from file_uploader.services import change_user_avatar
from file_uploader.utils.save_file import save_file

api_router = fa.APIRouter()


@api_router.post(
    "/add/{owner_type}/{owner_id}",
    response_class=ORJSONResponse,
    response_model=UploadFileResponse,
    status_code=fa.status.HTTP_200_OK,
    responses={
        fa.status.HTTP_200_OK: {
            "description": "ОК",
        },
        fa.status.HTTP_400_BAD_REQUEST: {
            "description": "Неверный формат запроса",
        },
        fa.status.HTTP_401_UNAUTHORIZED: {
            "description": "Запрос не авторизован",
        },
        fa.status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "В данный момент загрузка невозможна",
        },
    },
)
async def upload_files(
        owner_type: FileOwnerTypes = fa.Path(),
        owner_id: int = fa.Path(),
        file: fa.UploadFile = fa.File(),
        db: AsyncSession = fa.Depends(get_db),
) -> UploadFileResponse:
    """Загрузка файла.

    Файл прикрепляется к одному из допустимых типов обладателей.
    """
    # Если ничего не передано
    if file is None or file.filename == "":
        raise fa.HTTPException(fa.status.HTTP_400_BAD_REQUEST, detail="Файл не передан")

    # Сохранение файла на диск
    prepared_filename, file_size = await save_file(file, owner_type, owner_id)
    file.filename = prepared_filename
    file.size = file_size

    # Сохранение файлов в БД
    attached_file_id: int | None = await FilesCRUD.insert_file(
        db=db,
        file=file,
        owner_type=owner_type,
        owner_id=owner_id,
    )

    if attached_file_id is None:
        raise fa.HTTPException(fa.status.HTTP_503_SERVICE_UNAVAILABLE)

    if owner_type == FileOwnerTypes.USER:
        # Если это сохраняется аватарка пользователя, то сначала убеждаемся,
        # что они сохранились в сервисе пользователя, и только потом фиксируем изменения в БД.
        is_avatar_added: bool = await change_user_avatar(owner_id, file.filename)
        if is_avatar_added:
            await db.commit()
        else:
            raise fa.HTTPException(fa.status.HTTP_503_SERVICE_UNAVAILABLE,
                                   detail="Попробуйте позже. Удаленный сервис недоступен.")
    else:
        await db.commit()

    return UploadFileResponse(id=attached_file_id)

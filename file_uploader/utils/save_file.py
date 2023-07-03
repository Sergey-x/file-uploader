import os
import uuid
from pathlib import Path

import aiofiles
import fastapi as fa

from file_uploader.enums import FileOwnerTypes
from file_uploader.settings import SETTINGS

BAD_FILENAME_CHARS: str = "<>/|\\:&;?*"


async def save_file(file: fa.UploadFile, owner_type: FileOwnerTypes, owner_id: int) -> tuple[str, int] | None:
    """Save upload file in directory.

    Directory path relies on `owner_type`, `owner_id` params.
    """
    dest_dir: Path = SETTINGS.MEDIA_DIR / str(owner_type.name) / str(owner_id)
    os.makedirs(dest_dir, exist_ok=True)

    prepared_filename: str = prepare_filename(file.filename)
    if owner_type == FileOwnerTypes.USER:
        prepared_filename = str(uuid.uuid4().hex)

    dest_path: Path = dest_dir / prepared_filename

    async with aiofiles.open(dest_path, 'wb') as out_file:
        content = await file.read()
        file_size = len(content)
        await out_file.write(content)

    return prepared_filename, file_size


def prepare_filename(filename: str) -> str:
    new_filename: str = "".join(list(filter(lambda ch: ch not in BAD_FILENAME_CHARS, filename)))
    new_filename = new_filename.replace(" ", "_")
    return new_filename

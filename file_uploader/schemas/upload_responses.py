from datetime import datetime

import pydantic as pd


class LoadFileResponseItem(pd.BaseModel):
    id: int
    filename: str | None
    owner_id: int
    content_type: str
    dt_created: datetime | str
    size: int = 0


class GetEventFilesResponse(pd.BaseModel):
    files: list[LoadFileResponseItem]


class GetFileResponse(pd.BaseModel):
    file: LoadFileResponseItem


class UploadFileResponse(pd.BaseModel):
    id: int

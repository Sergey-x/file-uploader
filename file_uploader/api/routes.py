import fastapi as fa

from .v1 import delete_files, get_event_files, get_files, upload_files

api_router = fa.APIRouter()

api_router.include_router(get_event_files.api_router, prefix="/files", tags=["event-files"])
api_router.include_router(upload_files.api_router, prefix="/files", tags=["files"])
api_router.include_router(get_files.api_router, prefix="/files", tags=["files"])
api_router.include_router(delete_files.api_router, prefix="/files", tags=["files"])

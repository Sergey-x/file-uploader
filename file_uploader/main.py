import random
import string
import time

import fastapi as fa

from file_uploader.api import api_router
from file_uploader.db.db import MyDatabase
from file_uploader.logging import get_logger
from file_uploader.settings import SETTINGS

logger = get_logger(__name__)


def get_app() -> fa.FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = "Сервис для сохранения медиа-файлов."

    application = fa.FastAPI(
        title="File uploader",
        description=description,
        docs_url="/swagger",
        openapi_url="/openapi",
        version="0.1.0",
    )

    # add api routers
    application.include_router(api_router)

    # set handlers called when server start, stop
    application.add_event_handler("startup", MyDatabase.create_tables)

    # set settings
    application.state.settings = SETTINGS

    return application


app = get_app()


@app.middleware("http")
async def log_request(request: fa.Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("file_uploader.main:app", host="0.0.0.0", port=SETTINGS.MEDIA_POSTGRES_PORT, reload=True)

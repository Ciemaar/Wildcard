# ruff: noqa
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from wms.config import settings
from wms.database.seed import seed_data
from wms.database.session import AsyncSessionLocal
from wms.routers import dashboard, print_studio

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with AsyncSessionLocal() as session:
        await seed_data(session)
    yield


app = FastAPI(title="Wildcard Management System", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="src/wms/static"), name="static")
templates = Jinja2Templates(directory="src/wms/templates")
templates.env.globals["settings"] = settings

app.include_router(dashboard.router, prefix="/dashboard")
app.include_router(print_studio.router, prefix="/print-studio")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="base.html", context={"settings": settings}
    )


# noqa

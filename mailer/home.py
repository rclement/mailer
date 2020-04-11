from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .settings import Settings


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get(
    "/",
    summary="Homepage",
    description="Display homepage",
    response_class=HTMLResponse,
    include_in_schema=False,
)
def get_homepage(req: Request) -> HTMLResponse:
    settings: Settings = req.app.state.settings
    return templates.TemplateResponse(
        "homepage.html", dict(request=req, settings=settings)
    )

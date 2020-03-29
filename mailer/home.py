from fastapi import APIRouter, Request, Response
from fastapi.templating import Jinja2Templates

from .settings import Settings


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def get_homepage(req: Request) -> Response:
    settings: Settings = req.app.settings
    return templates.TemplateResponse(
        "homepage.html", dict(request=req, settings=settings)
    )

"""Idea Dashboard router."""

from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from wms.database.models import Mission
from wms.database.session import get_db

router = APIRouter(tags=["dashboard"])
templates = Jinja2Templates(directory="src/wms/templates")


@router.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    db: AsyncSession = Depends(get_db),
    status: str | None = None,
    category: str | None = None,
) -> HTMLResponse:
    """Render the dashboard with a list of missions."""
    query = select(Mission).order_by(Mission.created_at.desc())

    if status:
        query = query.where(Mission.status == status)
    if category:
        query = query.where(Mission.category == category)

    result = await db.execute(query)
    missions = result.scalars().all()

    cat_result = await db.execute(select(Mission.category).distinct())
    categories = cat_result.scalars().all()

    if request.headers.get("HX-Request"):
        return templates.TemplateResponse(
            request=request,
            name="partials/mission_table.html",
            context={"missions": missions},
        )

    from wms.config import settings

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "missions": missions,
            "categories": categories,
            "current_status": status,
            "current_category": category,
            "settings": settings,
        },
    )


@router.post("/mission", response_class=HTMLResponse)
async def add_prompt(
    request: Request,
    text: Annotated[str, Form()],
    category: Annotated[str, Form()],
    difficulty: Annotated[int, Form()],
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    """Add a new mission and return the updated table."""
    new_prompt = Mission(text=text, category=category, difficulty=difficulty)
    db.add(new_prompt)
    await db.commit()

    result = await db.execute(select(Mission).order_by(Mission.created_at.desc()))
    missions = result.scalars().all()

    return templates.TemplateResponse(
        request=request,
        name="partials/mission_table.html",
        context={"missions": missions},
    )


@router.patch("/mission/{mission_id}/status", response_class=HTMLResponse)
async def update_status(
    request: Request,
    mission_id: str,
    status: Annotated[str, Form()],
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    """Update a mission's status inline."""
    mission = await db.get(Mission, mission_id)
    if mission:
        mission.status = status
        await db.commit()

    return templates.TemplateResponse(
        request=request, name="partials/mission_row.html", context={"mission": mission}
    )


@router.delete("/mission/{mission_id}", response_class=HTMLResponse)
async def delete_prompt(
    mission_id: str,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    """Delete a mission."""
    mission = await db.get(Mission, mission_id)
    if mission:
        await db.delete(mission)
        await db.commit()

    return HTMLResponse(content="")

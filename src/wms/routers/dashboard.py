"""Idea Dashboard router."""

from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from wms.database.models import Prompt
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
    """Render the dashboard with a list of prompts."""
    query = select(Prompt).order_by(Prompt.created_at.desc())

    if status:
        query = query.where(Prompt.status == status)
    if category:
        query = query.where(Prompt.category == category)

    result = await db.execute(query)
    prompts = result.scalars().all()

    cat_result = await db.execute(select(Prompt.category).distinct())
    categories = cat_result.scalars().all()

    if request.headers.get("HX-Request"):
        return templates.TemplateResponse(
            request=request,
            name="partials/prompt_table.html",
            context={"prompts": prompts},
        )

    from wms.config import settings

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "prompts": prompts,
            "categories": categories,
            "current_status": status,
            "current_category": category,
            "settings": settings,
        },
    )


@router.post("/prompt", response_class=HTMLResponse)
async def add_prompt(
    request: Request,
    text: Annotated[str, Form()],
    category: Annotated[str, Form()],
    difficulty: Annotated[int, Form()],
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    """Add a new prompt and return the updated table."""
    new_prompt = Prompt(text=text, category=category, difficulty=difficulty)
    db.add(new_prompt)
    await db.commit()

    result = await db.execute(select(Prompt).order_by(Prompt.created_at.desc()))
    prompts = result.scalars().all()

    return templates.TemplateResponse(
        request=request, name="partials/prompt_table.html", context={"prompts": prompts}
    )


@router.patch("/prompt/{prompt_id}/status", response_class=HTMLResponse)
async def update_status(
    request: Request,
    prompt_id: str,
    status: Annotated[str, Form()],
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    """Update a prompt's status inline."""
    prompt = await db.get(Prompt, prompt_id)
    if prompt:
        prompt.status = status
        await db.commit()

    return templates.TemplateResponse(
        request=request, name="partials/prompt_row.html", context={"prompt": prompt}
    )


@router.delete("/prompt/{prompt_id}", response_class=HTMLResponse)
async def delete_prompt(
    prompt_id: str,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    """Delete a prompt."""
    prompt = await db.get(Prompt, prompt_id)
    if prompt:
        await db.delete(prompt)
        await db.commit()

    return HTMLResponse(content="")

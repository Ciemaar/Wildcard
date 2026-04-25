"""Print Studio router."""

from typing import Annotated, List

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from wms.database.models import Batch, BatchMission, Mission
from wms.database.session import get_db

router = APIRouter(tags=["print-studio"])
templates = Jinja2Templates(directory="src/wms/templates")


@router.get("/", response_class=HTMLResponse)
async def print_studio(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    """Render the print studio with all APPROVED missions."""
    # Only fetch approved missions for printing
    query = (
        select(Mission)
        .where(Mission.status == "APPROVED")
        .order_by(Mission.created_at.desc())
    )
    result = await db.execute(query)
    missions = result.scalars().all()

    from wms.config import settings

    return templates.TemplateResponse(
        request=request,
        name="print_studio.html",
        context={
            "missions": missions,
            "settings": settings,
        },
    )


@router.post("/batch", response_class=HTMLResponse)
async def create_batch(
    request: Request,
    batch_name: Annotated[str, Form()],
    mission_ids: Annotated[List[str], Form()] = [],
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    """Create a new batch from selected missions."""
    if not mission_ids:
        # User didn't select any
        return HTMLResponse(
            '<div class="rounded-md bg-red-50 p-4 mt-4"><div class="flex">'
            '<div class="ml-3"><h3 class="text-sm font-medium text-red-800">'
            "Error: No missions selected</h3></div></div></div>"
        )

    # 1. Create the Batch record
    new_batch = Batch(name=batch_name)
    db.add(new_batch)
    await db.flush()  # To get the batch.id generated

    # 2. Create the BatchMission join records
    for pid in mission_ids:
        bp = BatchMission(batch_id=new_batch.id, mission_id=pid)
        db.add(bp)

    await db.commit()

    # Provide a link to download the PDF for this batch,
    # or simply reload with success message
    from wms.config import settings

    return templates.TemplateResponse(
        request=request,
        name="partials/batch_success.html",
        context={"batch": new_batch, "settings": settings},
    )


@router.get("/batch/{batch_id}/pdf", response_class=Response)
async def generate_pdf(
    batch_id: str,
    db: AsyncSession = Depends(get_db),
) -> Response:
    """Generate a PDF for a specific batch."""
    from sqlalchemy.orm import selectinload
    from weasyprint import HTML

    from wms.config import settings

    # Fetch batch and its missions
    query = (
        select(Batch).where(Batch.id == batch_id).options(selectinload(Batch.missions))
    )
    result = await db.execute(query)
    batch = result.scalar_one_or_none()

    if not batch:
        return HTMLResponse("Batch not found", status_code=404)

    # Render HTML template for the PDF
    html_content = templates.TemplateResponse(
        request=Request(
            scope={"type": "http"}
        ),  # Mock request object for template rendering
        name="pdf_layout.html",
        context={
            "cards": batch.missions,
            "settings": settings,
        },
    ).body.decode("utf-8")

    # Generate PDF via WeasyPrint
    pdf_bytes = HTML(string=html_content).write_pdf()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="batch_{batch_id}.pdf"'},
    )

from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.contact import ContactMessage
from app.models.cv import CV
from app.services.email_service import send_contact_email

router = APIRouter(tags=["pages"])


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return render("index.html", request)


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CV).where(CV.is_active == True).order_by(CV.uploaded_at.desc()).limit(1))
    cv_record = result.scalar_one_or_none()
    return render("about.html", request, {"cv": cv_record})


@router.get("/projects", response_class=HTMLResponse)
async def projects(request: Request):
    return render("projects.html", request)


@router.get("/projects/rag", response_class=HTMLResponse)
async def project_rag(request: Request):
    return render("project_rag.html", request)


@router.get("/projects/anomaly-detection", response_class=HTMLResponse)
async def project_anomaly(request: Request):
    return render("project_anomaly.html", request)


@router.get("/projects/n8n-workflow", response_class=HTMLResponse)
async def project_n8n(request: Request):
    return render("project_n8n.html", request)


@router.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    return render("contact.html", request)


@router.post("/contact")
async def submit_contact(
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(None),
    message: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    entry = ContactMessage(name=name, email=email, subject=subject, message=message)
    db.add(entry)
    await db.commit()
    await send_contact_email(name, email, subject, message)
    return RedirectResponse(url="/contact?success=true", status_code=303)

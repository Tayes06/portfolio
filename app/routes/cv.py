import os
import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.cv import CV
from app.config import UPLOAD_DIR

router = APIRouter(prefix="/api/cv", tags=["cv"])

ALLOWED_EXTENSIONS = {".pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024


@router.post("/upload")
async def upload_cv(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Only PDF files are allowed")
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(400, "File exceeds 10MB limit")
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = UPLOAD_DIR / unique_name
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(content)
    result = await db.execute(select(CV).where(CV.is_active == True))
    old = result.scalars().all()
    for cv in old:
        cv.is_active = False
    record = CV(
        filename=unique_name,
        original_filename=file.filename,
        file_path=str(file_path),
        file_size=len(content),
        is_active=True,
    )
    db.add(record)
    await db.commit()
    return {"message": "CV uploaded successfully", "filename": unique_name}


@router.get("/download")
async def download_cv(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CV).where(CV.is_active == True).order_by(CV.uploaded_at.desc()).limit(1))
    cv = result.scalar_one_or_none()
    if not cv:
        raise HTTPException(404, "No CV found")
    return FileResponse(cv.file_path, media_type="application/pdf", filename=cv.original_filename)


@router.get("/preview")
async def preview_cv(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CV).where(CV.is_active == True).order_by(CV.uploaded_at.desc()).limit(1))
    cv = result.scalar_one_or_none()
    if not cv:
        raise HTTPException(404, "No CV found")
    return FileResponse(cv.file_path, media_type="application/pdf")

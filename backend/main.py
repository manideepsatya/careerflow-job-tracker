from sqlalchemy.orm import Session
from database import engine, get_db
import models
from fastapi import FastAPI, Depends, HTTPException
from datetime import date
from pydantic import BaseModel, Field
from typing import Literal
models.Base.metadata.create_all(bind=engine)
class JobApplication(BaseModel):
    company: str = Field(min_length=1)
    role: str = Field(min_length=1)
    location: str = Field(min_length=1)
    job_url: str = Field(min_length=1)
    notes: str = ""
    applied_date: date | None = None
    status: Literal["Interested", "Applied", "Assessment", "Interview", "Offer", "Rejected"]

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to CareerFlow"}
@app.get("/health")
def health_check():
    return {"status": "healthy"}
@app.post("/applications")
def create_application(application: JobApplication, db: Session = Depends(get_db)):
    db_application = models.JobApplication(
        company=application.company,
        role=application.role,
        location=application.location,
        job_url=application.job_url,
        notes=application.notes,
        applied_date=application.applied_date,
        status=application.status
)
    

    db.add(db_application)
    db.commit()
    db.refresh(db_application)

    return db_application
@app.get("/applications")
def get_applications(
    status: str | None = None,
    company: str | None = None,
    location: str | None = None,
    sort: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.JobApplication)

    if status:
        query = query.filter(models.JobApplication.status == status)

    if company:
        query = query.filter(models.JobApplication.company.ilike(f"%{company}%"))

    if location:
        query = query.filter(models.JobApplication.location.ilike(f"%{location}%"))

    if sort == "newest":
        query = query.order_by(
            models.JobApplication.applied_date.desc().nullslast()
        )

    elif sort == "oldest":
        query = query.order_by(
            models.JobApplication.applied_date.asc().nullslast()
        )
    return query.all()
@app.get("/applications/{application_id}")
def get_application(application_id: int, db: Session = Depends(get_db)):
    application = (
        db.query(models.JobApplication)
        .filter(models.JobApplication.id == application_id)
        .first()
    )

    if not application:
        raise HTTPException(
           status_code=404,
           detail="Application not found"
    )
    return application
@app.put("/applications/{application_id}")
def update_application(
    application_id: int,
    updated_application: JobApplication,
    db: Session = Depends(get_db)
):
    application = (
        db.query(models.JobApplication)
        .filter(models.JobApplication.id == application_id)
        .first()
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
    )

    application.company = updated_application.company
    application.role = updated_application.role
    application.location = updated_application.location
    application.job_url = updated_application.job_url
    application.notes = updated_application.notes
    application.applied_date = updated_application.applied_date
    application.status = updated_application.status

    db.commit()
    db.refresh(application)

    return application
@app.delete("/applications/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db)):
    application = (
        db.query(models.JobApplication)
        .filter(models.JobApplication.id == application_id)
        .first()
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
    )

    db.delete(application)
    db.commit()

    return {"message": "Application deleted successfully"}
from sqlalchemy.orm import Session
from database import engine, get_db
import models
from fastapi import FastAPI, Depends
from pydantic import BaseModel
models.Base.metadata.create_all(bind=engine)
class JobApplication(BaseModel):
    id: int
    company: str
    role: str
    status: str

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
        id=application.id,
        company=application.company,
        role=application.role,
        status=application.status
    )

    db.add(db_application)
    db.commit()
    db.refresh(db_application)

    return db_application
@app.get("/applications")
def get_applications(db: Session = Depends(get_db)):
    return db.query(models.JobApplication).all()
@app.get("/applications/{application_id}")
def get_application(application_id: int, db: Session = Depends(get_db)):
    application = (
        db.query(models.JobApplication)
        .filter(models.JobApplication.id == application_id)
        .first()
    )

    if application:
        return application

    return {"message": "Application not found"}
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
        return {"message": "Application not found"}

    application.company = updated_application.company
    application.role = updated_application.role
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
        return {"message": "Application not found"}

    db.delete(application)
    db.commit()

    return {"message": "Application deleted successfully"}
from fastapi import FastAPI
from pydantic import BaseModel
class JobApplication(BaseModel):
    id: int
    company: str
    role: str
    status: str

applications = []
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to CareerFlow"}
@app.get("/health")
def health_check():
    return {"status": "healthy"}
@app.post("/applications")
def create_application(application: JobApplication):
    applications.append(application)
    return application
@app.get("/applications")
def get_applications():
    return applications
@app.get("/applications/{application_id}")
def get_application(application_id: int):
    for application in applications:
        if application.id == application_id:
            return application
    return {"message": "Application not found"}
@app.put("/applications/{application_id}")
def update_application(application_id: int, updated_application: JobApplication):
    for index, application in enumerate(applications):
        if application.id == application_id:
            applications[index] = updated_application
            return updated_application

    return {"message": "Application not found"}
@app.delete("/applications/{application_id}")
def delete_application(application_id: int):
    for index, application in enumerate(applications):
        if application.id == application_id:
            deleted_application = applications.pop(index)
            return deleted_application

    return {"message": "Application not found"}
from fastapi import FastAPI, Body, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException

import database
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from pydantic import BaseModel

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="form"))


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    return FileResponse("form/form.html")


@app.post("/submit")
def submit(data = Body(), db: Session = Depends(get_db)):
    report = database.Report(theme=data["theme"], title=data["title"], details=data["details"])

    db.add(report)

    try:
        db.commit()
        db.refresh(report)

        return {"status": "saved"}
    
    except IntegrityError:
        return {"status": "skipped", "reason": "exists"}


@app.get("/reports")
def get_reports(db: Session = Depends(get_db)):
    return db.query(database.Report).all()


class ReportModel(BaseModel):
    title: str
    details: str


@app.post("/delete")
def delete_report(data: ReportModel = Body(), db: Session = Depends(get_db)):
    title = data.title
    details = data.details

    report_to_delete = db.query(database.Report).filter_by(
        title=title,
        details=details
    ).first()

    if not report_to_delete:
        raise HTTPException(status_code=404, detail="Report doesn't exist")
    
    db.delete(report_to_delete)
    db.commit()

    return {"status": "deleted"}
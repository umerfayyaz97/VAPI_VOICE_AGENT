#step1: import database objects

from sqlalchemy import Column, Column

from sqlalchemy import Integer

from database import init_db, Appointment # to put data in appointment class and to call database function to create tables if not exist

init_db() 

#step3: Create Datac contracts using pydantic models ( linking to step 2)
import datetime as dt 
from pydantic import BaseModel

class AppointmentRequest(BaseModel):
    patient_name: str
    reason: str
    start_time: dt.datetime

class AppointmentResponse(BaseModel):
        id: int
        patient_name: str
        reason: str | None
        start_time: dt.datetime
        cancelled: bool 
        created_at: dt.datetime

class CancelAppointmentRequest(BaseModel):
    patient_name: str
    date: dt.datetime

class cancelAppointmentResponse(BaseModel):
    cancelled_count: int

#step2: cretae FASTAPI app endpoints pseudo code

from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()

#schedule_appt
@app.post("/schedule_appointments/")
def schedule_appointment(appointment: AppointmentRequest):
    #logic to schedule appointment
    return

#cancel_appt
@app.put("/cancel_appointments/")
def cancel_appointment():
    #logic to cancel appointment
    return

#list_appt
@app.get("/list_appointments/")
def list_appointments():
    #logic to get appointments
    return




#step4: Write actual code
#step5: Create streamlit (just for testing)


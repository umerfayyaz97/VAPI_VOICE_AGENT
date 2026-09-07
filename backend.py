#step1: import database objects

from sqlalchemy import Column

from sqlalchemy import Integer

from database import init_db, Appointment, get_db # to put data in appointment class and to call database function to create tables if not exist
from sqlalchemy.orm import Session

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

class CancelAppointmentResponse(BaseModel):
    cancelled_count: int

#step2: cretae FASTAPI app endpoints pseudo code

from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()

#schedule_appt
@app.post("/schedule_appointments/")
def schedule_appointment(request: AppointmentRequest, db: Session = Depends(get_db)):
    new_appointment = Appointment(
        patient_name = request.patient_name,
        reason = request.reason,
        start_time = request.start_time
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    new_appointment_response = AppointmentResponse(
        id=new_appointment.id,
        patient_name=new_appointment.patient_name,
        reason=new_appointment.reason,
        start_time=new_appointment.start_time,
        cancelled=new_appointment.cancelled,
        created_at=new_appointment.created_at
    )

    return new_appointment_response


#cancel_appt
from sqlalchemy import select
@app.put("/cancel_appointments/")
def cancel_appointment(request: CancelAppointmentRequest, db: Session = Depends(get_db)):

    start_dt = dt.datetime.combine(request.date, dt.time.min)
    end_dt = dt.datetime.combine(request.date, dt.time.max)

    result = db.execute(
    select(Appointment)
    .where(Appointment.patient_name == request.patient_name)
    .where(Appointment.start_time >= start_dt)        
    .where(Appointment.start_time < end_dt)
    .where(Appointment.cancelled ==False)        
    )

    appointments = result.scalars().all()
    if not appointments:
        raise HTTPException(status_code=404, detail="No appointments found for the given patient and date.")
    
    

    #logic to cancel appointment
    return

#list_appt
@app.get("/list_appointments/")
def list_appointments():
    #logic to get appointments
    return




#step4: Write actual code
#step5: Create streamlit (just for testing)


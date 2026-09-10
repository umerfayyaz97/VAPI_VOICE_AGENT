#step1: import database objects

from sqlalchemy import Column
from fastapi import Depends
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

class ListAppointmentsRequest(BaseModel):
    date: dt.date

#step2: cretae FASTAPI app endpoints pseudo code

from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()


# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import JSONResponse
# from fastapi import Request

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     # This will print the exact JSON Vapi sent and the exact error!
#     body = await request.body()
#     print(f"\n--- 422 ERROR DEBUGGER ---")
#     print(f"VAPI SENT THIS: {body.decode()}")
#     print(f"PYDANTIC ERROR: {exc.errors()}")
#     print(f"--------------------------\n")
#     return JSONResponse(status_code=422, content={"detail": exc.errors()})

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
@app.post("/cancel_appointments/")
def cancel_appointment(request: CancelAppointmentRequest, db: Session = Depends(get_db)):

    start_dt = dt.datetime.combine(request.date, dt.time.min)
    end_dt = start_dt + dt.timedelta(days=1)

    result = db.execute(
    select(Appointment)
    .where(Appointment.patient_name == request.patient_name)
    .where(Appointment.start_time >= start_dt)        
    .where(Appointment.start_time < end_dt)
    .where(Appointment.cancelled ==False)        
    )

    appointments = result.scalars().all()
    #if no appointments found for the given patient and date, raise an HTTPException with status code 404 and a detail message
    if not appointments:
        raise HTTPException(status_code=404, detail="No appointments found for the given patient and date.")
    
    #if appointments are found, iterate through the list of appointments and set the cancelled attribute to True for each appointment. Then commit the changes to the database and return a CancelAppointmentResponse with the count of cancelled appointments.
    for appointment in appointments:
         appointment.cancelled = True

    db.commit()

   
    return CancelAppointmentResponse(cancelled_count=len(appointments))

#list_appt
@app.post("/list_appointments/")
def list_appointments(request: ListAppointmentsRequest , db : Session = Depends(get_db)):

    start_dt = dt.datetime.combine(request.date , dt.time.min)
    end_dt = start_dt + dt.timedelta(days=1)

    result = db.execute(
    select(Appointment)
    .where(Appointment.cancelled == False)
    .where(Appointment.start_time >= start_dt)        
    .where(Appointment.start_time < end_dt)
    .order_by(Appointment.start_time.asc())

    )

    booked_appointment = []
    for appointment in result.scalars():
        appointment_obj = AppointmentResponse(
        id=appointment.id,
        patient_name=appointment.patient_name,
        reason=appointment.reason,
        start_time=appointment.start_time,
        cancelled=appointment.cancelled,
        created_at=appointment.created_at
     ) 
        booked_appointment.append(appointment_obj)
    
    return booked_appointment

import uvicorn  
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="127.0.0.1", port=8000, reload=True)




#step4: Write actual code
#step5: Create streamlit (just for testing)


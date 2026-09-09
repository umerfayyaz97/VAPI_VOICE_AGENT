import streamlit as st
import requests
import datetime
import pandas as pd

st.set_page_config(page_title="Appointment Backend Tester", layout="centered")

# ==========================================
# SIDEBAR: CONFIGURATION
# ==========================================
st.sidebar.header("⚙️ Configuration")
# Input field for the Base URL
raw_url = st.sidebar.text_input("Backend API URL", value="http://127.0.0.1:8000")
# Remove any trailing slashes just in case you accidentally type one (e.g., "http://127.0.0.1:8000/")
BASE_URL = raw_url.rstrip("/")

st.sidebar.markdown("---")
st.sidebar.info(f"Currently targeting:\n`{BASE_URL}`")

st.title("🏥 Appointment System Backend Tester")
st.markdown("Use this interface to interact with your FastAPI backend and test the endpoints.")

# ==========================================
# SECTION 1: SCHEDULE APPOINTMENT
# ==========================================
st.header("1. Schedule Appointment")
with st.container(border=True):
    with st.form("schedule_form"):
        sch_name = st.text_input("Patient Name")
        sch_reason = st.text_area("Reason for Visit")
        
        col1, col2 = st.columns(2)
        with col1:
            sch_date = st.date_input("Start Date")
        with col2:
            sch_time = st.time_input("Start Time")
            
        submit_schedule = st.form_submit_button("Schedule Appointment", type="primary")
        
        if submit_schedule:
            if not sch_name or not sch_reason:
                st.error("Please provide both a name and a reason.")
            else:
                start_datetime = datetime.datetime.combine(sch_date, sch_time).isoformat()
                
                payload = {
                    "patient_name": sch_name,
                    "reason": sch_reason,
                    "start_time": start_datetime
                }
                
                try:
                    response = requests.post(f"{BASE_URL}/schedule_appointments/", json=payload)
                    if response.status_code == 200:
                        st.success("Appointment Scheduled Successfully!")
                        st.json(response.json())
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error(f"Failed to connect to backend at {BASE_URL}. Is it running?")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

# ==========================================
# SECTION 2: LIST APPOINTMENTS (BY DATE)
# ==========================================
st.header("2. List Appointments")
with st.container(border=True):
    with st.form("fetch_form"):
        fetch_date = st.date_input("Select Date to View Bookings")
        submit_fetch = st.form_submit_button("Fetch Bookings")
        
        if submit_fetch:
            params = {"date": fetch_date.isoformat()}
            
            try:
                response = requests.get(f"{BASE_URL}/list_appointments/", params=params)
                if response.status_code == 200:
                    appointments = response.json()
                    if appointments:
                        st.success(f"Found {len(appointments)} appointment(s)!")
                        
                        df = pd.DataFrame(appointments)
                        df['start_time'] = pd.to_datetime(df['start_time']).dt.strftime('%I:%M %p')
                        
                        st.dataframe(
                            df[['id', 'patient_name', 'reason', 'start_time']], 
                            use_container_width=True,
                            hide_index=True
                        )
                    else:
                        st.info(f"No appointments found for {fetch_date}.")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error(f"Failed to connect to backend at {BASE_URL}. Is it running?")
            except Exception as e:
                st.error(f"An error occurred: {e}")

# ==========================================
# SECTION 3: CANCEL APPOINTMENT
# ==========================================
st.header("3. Cancel Appointment")
with st.container(border=True):
    with st.form("cancel_form"):
        cancel_name = st.text_input("Patient Name")
        cancel_date = st.date_input("Date of Appointment to Cancel")
        
        submit_cancel = st.form_submit_button("Cancel Appointment")
        
        if submit_cancel:
            if not cancel_name:
                st.error("Please provide a patient name.")
            else:
                cancel_datetime = datetime.datetime.combine(cancel_date, datetime.time.min).isoformat()
                
                payload = {
                    "patient_name": cancel_name,
                    "date": cancel_datetime
                }
                
                try:
                    response = requests.post(f"{BASE_URL}/cancel_appointments/", json=payload)
                    if response.status_code == 200:
                        count = response.json().get('cancelled_count', 0)
                        st.success(f"Successfully cancelled {count} appointment(s)!")
                    elif response.status_code == 404:
                        st.warning("No appointments found to cancel for the given patient and date.")
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error(f"Failed to connect to backend at {BASE_URL}. Is it running?")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
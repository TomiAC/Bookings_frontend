import streamlit as st
from datetime import datetime, date, timedelta
import login
import requests

login.generateLogin()
if 'access_token' in st.session_state:
    st.title("Booking App")
    st.divider()

    st.subheader("Active bookings")
    headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
    bookings = requests.get('http://127.0.0.1:5000/reservations/active_bookings', headers=headers)
    for booking in bookings:
        with st.container(border=True):
            st.subheader('Court')
            st.text(bookings.json()[0].get('court_name'))
            columns_bookings = st.columns([5,5,5])
            with columns_bookings[0]:
                st.subheader('Date')
                st.text(bookings.json()[0].get('date'))
            with columns_bookings[1]:
                st.subheader('Time')
                st.text(bookings.json()[0].get('time'))
            with columns_bookings[2]:
                st.subheader('Duration')
                st.text(bookings.json()[0].get('duration'))

    all_dates = []
    start_dt = datetime.now()
    delta = timedelta(days=1)
    for i in range(90):
        all_dates.append(start_dt.strftime("%d/%m/%Y"))
        start_dt+=delta

    st.divider()

    st.subheader("Add new booking")
    with st.form('frmBooking'):
        booking_date = st.selectbox('Select date', options=all_dates)

        all_hours = [x for x in range(10, 24)]
        booking_hour = st.selectbox('Start hour', options=all_hours)

        booking_duration = st.select_slider('Duration', options=[1, 2, 3, 4, 5])

        courts = requests.get('http://127.0.0.1:5000/courts/list_all', headers=headers)
        courts_id = []
        for court in courts.json():
            courts_id.append(court['id'])

        booking_court = st.selectbox('Court', options=courts_id, format_func=lambda x: next((dic['identificador'] for dic in courts.json() if dic.get('id') == x), None))

        btn_booking = st.form_submit_button('Book', type='primary')

        if btn_booking:
            data = {"date": booking_date,
                    "time": booking_hour,
                    "duration": booking_duration,
                    "court_id": booking_court}
            print(data)
            requests.post('http://127.0.0.1:5000/reservations/book', headers=headers, json=data)
            


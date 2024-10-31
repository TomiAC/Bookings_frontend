import streamlit as st
import login

st.header("Inicie Sesion")
login.generateLogin()
if 'access_token' in st.session_state:
    st.subheader('Información página principal')
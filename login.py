import streamlit as st
import requests

def validarUsuario(email, password):    
    """Permite la validación de usuario y clave

    Args:
        usuario (str): usuario a validar
        clave (str): clave del usuario

    Returns:
        bool: True usuario valido, False usuario invalido
    """
    data = {
        "email": email,
        "password": password

    }
    response = requests.post("http://127.0.0.1:5000/auth/login", json=data)
    status_code = response.status_code
    result = response.json()

    if status_code==200:
        return {'access_token': result['access_token'],
                'refresh_token': result['refresh_token']}
    else:
        return False
    
    #Manejar errores

def generateMenu():
    """Genera el menú dependiendo del usuario

    Args:
        usuario (str): usuario utilizado para generar el menú
    """        
    with st.sidebar:
        st.write(f"Hola")
        # Mostramos los enlaces de páginas
        st.page_link("inicio.py", label="Inicio", icon=":material/home:")
        st.subheader("Tableros")
        st.page_link("pages/bookings.py", label="Reservas", icon=":material/sell:")
        # Botón para cerrar la sesión
        btnSalir=st.button("Salir")
        if btnSalir:
            st.session_state.clear()
            # Luego de borrar el Session State reiniciamos la app para mostrar la opción de usuario y clave
            st.rerun()


def generateLogin():
    """
    Genera la ventana de login o muestra el menú si el login es valido
    """    
    # Validamos si el usuario ya fue ingresado    
    if 'access_token' in st.session_state:
        generateMenu() # Si ya hay usuario cargamos el menu        
    else: 
        # Cargamos el formulario de login       
        with st.form('frmLogin'):
            email = st.text_input('Email')
            password = st.text_input('Password',type='password')
            btn_login=st.form_submit_button('Ingresar',type='primary')
            if btn_login:
                token = validarUsuario(email,password)
                if token:
                    st.session_state['access_token'] = token['access_token']
                    st.session_state['refresh_token'] = token['refresh_token']
                    # Si el usuario es correcto reiniciamos la app para que se cargue el menú
                    st.rerun()
                else:
                    # Si el usuario es invalido, mostramos el mensaje de error
                    st.error("Usuario o clave inválidos", icon=":material/gpp_maybe:")
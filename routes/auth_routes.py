from flask import Blueprint, render_template, redirect, request, session, url_for
import requests

auth_bp = Blueprint('auth', __name__)

API_BASE_URL = "http://localhost:5002"  # Cambia al puerto donde corre tu API FastAPI

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario_ingresado = request.form.get('usuario')
        contrasena_ingresada = request.form.get('contrasena')

        try:
            response = requests.get(f"{API_BASE_URL}/usuarios/")
            if response.status_code == 200:
                usuarios = response.json()
                # Validar si existe el usuario
                for usuario in usuarios:
                    if usuario['usuario'] == usuario_ingresado and usuario['contrasena'] == contrasena_ingresada:
                        session['usuario'] = usuario['usuario']
                        session['rol'] = usuario['rol']  # Si manejas roles
                        # Redirige según el rol
                        if usuario['rol'] == 'admin':
                            return redirect(url_for('admin.dashboard'))
                        elif usuario['rol'] == 'proveedor':
                            return redirect(url_for('proveedor.dashboard'))
                        else:
                            return redirect(url_for('cliente.dashboard'))
                return render_template('login.html', mensaje="Usuario o contraseña incorrectos.")
            else:
                return render_template('login.html', mensaje="Error al conectar con la API.")
        except Exception as e:
            return render_template('login.html', mensaje=f"Error: {str(e)}")
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

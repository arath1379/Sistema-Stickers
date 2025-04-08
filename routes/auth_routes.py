from flask import Flask, render_template, request, redirect, url_for, session, flash,Blueprint
import requests

auth_bp = Blueprint('auth', __name__)
API_BASE_URL = "http://localhost:5002"  # Dirección de tu API

# Diccionario de roles por correo (solo usado para login en frontend)
roles_por_correo = {
    'juan@gmail.com': 'cliente',
    'maria@gmail.com': 'proveedor',
    'ana@gmail.com': 'admin',
    'pedro@hotmail.com': 'cliente',
    'laura@hotmail.com': 'proveedor',
    'josucampos157@gmail.com': 'cliente',
}

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        rol_input = request.form['rol']  # Este viene del campo del formulario

        # Obtener usuarios desde la API
        response = requests.get("http://localhost:5002/usuarios")
        usuarios = response.json()

        for usuario in usuarios:
            if usuario['correo'] == correo:
                # Validación simple: si el correo existe
                session['usuario'] = correo
                session['usuario_id'] = usuario['id']
                session['rol'] = rol_input.strip().lower()  # 👉 Esta línea es la clave

                # Redireccionar según el rol
                if session['rol'] == 'cliente':
                    return redirect(url_for('cliente.dashboard'))
                elif session['rol'] == 'proveedor':
                    return redirect(url_for('proveedor.dashboard'))
                elif session['rol'] == 'admin':
                    return redirect(url_for('admin.dashboard'))

        flash('Correo no válido o no encontrado', 'error')
    return render_template('login.html')

@auth_bp.route('/registrar', methods=['POST'])
def registrar():
    # Obtener datos del formulario del modal
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    rol = request.form.get('rol')

    try:
        # Enviar datos a la API para registrar (ajusta el endpoint según tu API)
        response = requests.post(f"{API_BASE_URL}/usuarios/", json={
            "nombre": nombre,
            "correo": correo
        })

        if response.status_code == 201:
            # Agregar el nuevo correo y rol al diccionario
            roles_por_correo[correo.lower()] = rol.lower()
            return redirect(url_for('auth.login'))
        else:
            return render_template('login.html', mensaje="Error al registrar usuario.")
    except Exception as e:
        return render_template('login.html', mensaje=f"Error: {str(e)}")

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint 
import requests

auth_bp = Blueprint('auth', __name__)
API_BASE_URL = "http://localhost:5002"  # Dirección de tu API

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        rol_input = request.form['rol']  # Este viene del campo del formulario

        # Obtener usuarios desde la API
        response = requests.get(f"{API_BASE_URL}/usuarios")
        usuarios = response.json()

        for usuario in usuarios:
            if usuario['correo'] == correo:
                session['usuario'] = correo
                session['usuario_id'] = usuario['id']
                session['rol'] = rol_input.strip().lower()  # Rol desde el formulario

                # Redireccionar según el rol
                if session['rol'] == 'cliente':
                    return redirect(url_for('cliente.dashboard'))
                elif session['rol'] == 'proveedor':
                    return redirect(url_for('proveedor.dashboard'))
                elif session['rol'] == 'admin':
                    return redirect(url_for('admin.dashboard'))

        flash('Correo no válido o no encontrado', 'error')
    return render_template('login.html')

@auth_bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'GET':
        return redirect(url_for('auth.login'))  # O mostrar algún mensaje

    # POST: lógica de registro
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    rol = request.form.get('rol')
    contrasena = request.form.get('contrasena')

    try:
        response = requests.post(f"{API_BASE_URL}/usuarios/", json={
            "nombre": nombre,
            "correo": correo,
            "rol": rol.lower(),
            "contrasena": contrasena
        })

        if response.status_code == 201:
            return redirect(url_for('auth.login'))
        else:
            return render_template('login.html', mensaje="Error al registrar usuario.")
    except Exception as e:
        return render_template('login.html', mensaje=f"Error: {str(e)}")


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

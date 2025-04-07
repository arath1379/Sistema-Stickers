from flask import Blueprint, render_template, redirect, request, session

auth_bp = Blueprint('main', __name__)

@auth_bp.route('/')
def login():
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@auth_bp.route('/registro', methods=['POST'])
def registro():
    nombre = request.form['nombre']
    correo = request.form['correo']
    contrasena = request.form['contrasena']
    
    if not nombre or not correo or not contrasena:
        return render_template('registro.html', mensaje="Todos los campos son obligatorios.")
    
    return redirect('/login')
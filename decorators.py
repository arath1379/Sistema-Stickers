from functools import wraps
from flask import session, redirect, url_for, flash

def login_requerido(rol=None):
    def decorador(f):
        @wraps(f)
        def funcion(*args, **kwargs):
            if 'usuario_id' not in session:
                flash("Debes iniciar sesión")
                return redirect(url_for('main.login'))
            if rol and session.get('rol') != rol:
                flash("Acceso no autorizado")
                return redirect(url_for('main.login'))
            return f(*args, **kwargs)
        return funcion
    return decorador

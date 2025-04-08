from flask import Blueprint, render_template, session
from services.productos_service import listar_productos

cliente_bp = Blueprint('cliente', __name__, url_prefix='/cliente')

@cliente_bp.route('/dashboard')
def dashboard():
    if session.get('rol') != 'cliente':
        return "Acceso denegado", 403
    return render_template('templatesUser/cliente.html')

@cliente_bp.route('/catalogo')
def catalogo():
    productos = listar_productos()
    return render_template('templatesUser/catalogo.html', productos=productos)

@cliente_bp.route('/carrito')
def carrito():
    return render_template('templatesUser/carrito.html')

@cliente_bp.route('/historial')
def historial():
    return render_template('templatesUser/historial.html')

@cliente_bp.route('/pedidos')
def pedidos():
    return render_template('templatesUser/pedidos.html')

@cliente_bp.route('/perfil')
def perfil():
    return render_template('templatesUser/perfil.html')
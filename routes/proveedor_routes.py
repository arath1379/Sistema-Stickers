from flask import Blueprint, render_template, session
from services.clientes_service import listar_clientes
from services.inventario_service import listar_inventario
from services.pedidos_service import listar_pedidos

proveedor_bp = Blueprint('proveedor', __name__, url_prefix='/proveedor')

@proveedor_bp.route('/dashboard')
def dashboard():
    if session.get('rol') != 'proveedor':
        return "Acceso denegado", 403
    return render_template('templatesProveedor/proveedor.html')

@proveedor_bp.route('/clientes')
def proveedor_clientes():
    clientes = listar_clientes()
    return render_template('templatesProveedor/Gestion_Clientes.html', clientes=clientes)

@proveedor_bp.route('/inventario')
def proveedor_inventario():
    inventario = listar_inventario()
    return render_template('templatesProveedor/Gestion_inventario.html', inventario=inventario)

@proveedor_bp.route('/pedidos')
def proveedor_pedidos():
    pedidos = listar_pedidos()
    return render_template('templatesProveedor/Gestion_pedidos.html', pedidos=pedidos)

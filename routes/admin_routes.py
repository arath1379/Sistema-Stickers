from flask import Blueprint, render_template, request, redirect, url_for
from services.usuarios_service import listar_usuarios
from services.clientes_service import listar_clientes
from services.proveedores_service import listar_proveedores
from services.roles_service import listar_roles
from services.reportes_service import listar_reportes

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def dashboard_admin():
    return render_template('templatesAdmin/admin.html')

@admin_bp.route('/clientes')
def admin_clientes():
    clientes = listar_clientes()
    return render_template('templatesAdmin/Gestion_cliente.html', clientes=clientes)

@admin_bp.route('/proveedores')
def admin_proveedores():
    proveedores = listar_proveedores()
    return render_template('templatesAdmin/Gestion_proveedores.html', proveedores=proveedores)

@admin_bp.route('/roles')
def admin_roles():
    roles = listar_roles()
    return render_template('templatesAdmin/Gestion_roles.html', roles=roles)

@admin_bp.route('/reportes')
def admin_reportes():
    reportes = listar_reportes()
    return render_template('templatesAdmin/Reportes_estadisticas.html', reportes=reportes)

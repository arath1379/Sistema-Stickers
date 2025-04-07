from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from requests import get, post

main = Blueprint('main', __name__)

FASTAPI_URL = "http://localhost:5001"  # Cambia si usas otro puerto/host

# ----------- Funciones Generales -----------

def get_data(endpoint):
    try:
        response = get(f"{FASTAPI_URL}{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR GET {endpoint}]: {e}")
        return None

def post_data(endpoint, data):
    try:
        response = post(f"{FASTAPI_URL}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR POST {endpoint}]: {e}")
        return None

# ----------- Rutas para Productos -----------

@main.route('/productos')
def productos():
    productos = get_data("/productos/")
    if productos:
        return render_template('productos.html', productos=productos)
    else:
        flash("No se pudieron cargar los productos.", "error")
        return redirect(url_for('main.dashboard_admin'))

@main.route('/producto/crear', methods=['POST'])
def crear_producto():
    nombre = request.form['nombre']
    precio = float(request.form['precio'])
    descripcion = request.form['descripcion']
    
    producto = {"nombre": nombre, "precio": precio, "descripcion": descripcion}
    
    result = post_data("/productos/", producto)
    
    if result:
        flash("Producto creado con éxito", "success")
    else:
        flash("Error al crear el producto.", "error")
    
    return redirect(url_for('main.productos'))

# ----------- Rutas para Clientes -----------

@main.route('/clientes')
def clientes():
    clientes = get_data("/clientes/")
    if clientes:
        return render_template('clientes.html', clientes=clientes)
    else:
        flash("No se pudieron cargar los clientes.", "error")
        return redirect(url_for('main.dashboard_admin'))

@main.route('/cliente/crear', methods=['POST'])
def crear_cliente():
    nombre = request.form['nombre']
    correo = request.form['correo']
    direccion = request.form['direccion']
    
    cliente = {"nombre": nombre, "correo": correo, "direccion": direccion}
    
    result = post_data("/clientes/", cliente)
    
    if result:
        flash("Cliente creado con éxito", "success")
    else:
        flash("Error al crear el cliente.", "error")
    
    return redirect(url_for('main.clientes'))

# ----------- Rutas para Pedidos -----------

@main.route('/pedidos')
def pedidos():
    pedidos = get_data("/pedidos/")
    if pedidos:
        return render_template('pedidos.html', pedidos=pedidos)
    else:
        flash("No se pudieron cargar los pedidos.", "error")
        return redirect(url_for('main.dashboard_admin'))

@main.route('/pedido/crear', methods=['POST'])
def crear_pedido():
    cliente_id = request.form['cliente_id']
    productos = request.form.getlist('productos')
    total = float(request.form['total'])
    
    pedido = {"cliente_id": cliente_id, "productos": productos, "total": total}
    
    result = post_data("/pedidos/", pedido)
    
    if result:
        flash("Pedido creado con éxito", "success")
    else:
        flash("Error al crear el pedido.", "error")
    
    return redirect(url_for('main.pedidos'))

# ----------- Rutas para Reportes -----------

@main.route('/reportes')
def reportes():
    reportes = get_data("/reportes/")
    if reportes:
        return render_template('reportes.html', reportes=reportes)
    else:
        flash("No se pudieron cargar los reportes.", "error")
        return redirect(url_for('main.dashboard_admin'))

@main.route('/reporte/crear', methods=['POST'])
def crear_reporte():
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    
    reporte = {"titulo": titulo, "descripcion": descripcion}
    
    result = post_data("/reportes/", reporte)
    
    if result:
        flash("Reporte creado con éxito", "success")
    else:
        flash("Error al crear el reporte.", "error")
    
    return redirect(url_for('main.reportes'))

# ----------- Rutas para Roles -----------

@main.route('/roles')
def roles():
    roles = get_data("/roles/")
    if roles:
        return render_template('roles.html', roles=roles)
    else:
        flash("No se pudieron cargar los roles.", "error")
        return redirect(url_for('main.dashboard_admin'))

@main.route('/rol/crear', methods=['POST'])
def crear_rol():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    
    rol = {"nombre": nombre, "descripcion": descripcion}
    
    result = post_data("/roles/", rol)
    
    if result:
        flash("Rol creado con éxito", "success")
    else:
        flash("Error al crear el rol.", "error")
    
    return redirect(url_for('main.roles'))

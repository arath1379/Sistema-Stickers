from flask import Blueprint, render_template, session, request, redirect, url_for, flash
import requests

from services.clientes_service import listar_clientes
from services.pedidos_service import listar_pedidos

proveedor_bp = Blueprint('proveedor', __name__, url_prefix='/proveedor')

API_URL = "http://localhost:5002"  # Cambia si tu API tiene otro host o puerto

@proveedor_bp.route('/dashboard')
def dashboard():
    if session.get('rol') != 'proveedor':
        return "Acceso denegado", 403
    return render_template('templatesProveedor/proveedor.html')

@proveedor_bp.route('/clientes')
def proveedor_clientes():
    clientes = listar_clientes()
    return render_template('templatesProveedor/Gestion_Clientes.html', clientes=clientes)

@proveedor_bp.route('/pedidos')
def proveedor_pedidos():
    pedidos = listar_pedidos()
    return render_template('templatesProveedor/Gestion_pedidos.html', pedidos=pedidos)

# Listar productos
@proveedor_bp.route('/productos')
def proveedor_productos():
    try:
        response = requests.get(API_URL + "/productos/")  # Endpoint para listar productos
        productos = response.json()

        print("🔍 Productos recibidos desde la API:")
        print(productos)

    except Exception as e:
        productos = []
        flash("Error al obtener productos: " + str(e))
    return render_template('templatesProveedor/Gestion_inventario.html', productos=productos)

# Agregar producto
@proveedor_bp.route('/productos', methods=['POST'])
def agregar_producto():
    data = {
        "nombre": request.form['nombre'],
        "categoria": request.form['categoria'],
        "precio": float(request.form['precio']),
        "stock": int(request.form['stock'])
    }
    try:
        # Realiza la solicitud POST a /productos/ para agregar el producto
        response = requests.post(API_URL + "/productos/", json=data)

        if response.status_code == 200:
            flash("Producto agregado exitosamente.")
        else:
            flash("Error al agregar producto.")
    except Exception as e:
        flash("Error: " + str(e))

    # Redirige a la página de inventario
    return redirect(url_for('proveedor.proveedor_productos'))

# Editar producto
@proveedor_bp.route('/productos/editar/<int:id>', methods=['POST'])
def editar_producto(id):
    # Obtener los datos del formulario con get() para evitar errores si falta alguna clave
    nombre = request.form.get('nombre', '')
    categoria = request.form.get('categoria', '')
    precio = request.form.get('precio', 0)
    stock = request.form.get('stock', 0)  # Cambié 'cantidad' por 'stock'

    # Convertir los datos correctamente
    try:
        precio = float(precio)
        stock = int(stock)  # Aseguramos que 'stock' se convierte correctamente
    except ValueError:
        flash("Los datos proporcionados son incorrectos.")
        return redirect(url_for('proveedor.proveedor_productos'))

    data = {
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "stock": stock  # Aseguramos que 'stock' es el campo enviado
    }

    try:
        # Obtener todos los productos y filtrar por id
        response = requests.get(f"{API_URL}/productos/")  # Obtener todos los productos
        productos = response.json()

        # Buscar el producto con el ID correspondiente
        producto_actual = next((producto for producto in productos if producto['id'] == id), None)

        if not producto_actual:
            flash("Producto no encontrado.")
            return redirect(url_for('proveedor.proveedor_productos'))

        # Si se encontró el producto, ajustamos el stock
        stock_actual = producto_actual.get('stock', 0)  # Cambié 'cantidad' por 'stock'
        if stock != stock_actual:  # Solo actualizar si hay un cambio
            # Realizar una solicitud PUT para ajustar el stock
            response = requests.put(f"{API_URL}/productos/{id}/ajustar_stock?cantidad={stock}", json={})
            if response.status_code == 200:
                flash("Stock del producto ajustado correctamente.")
            else:
                flash("Error al ajustar el stock.")
        else:
            flash("No se realizó ningún cambio en el stock.")

        # Si también se quiere cambiar el nombre, categoría y precio, se puede hacer una actualización de todo el producto
        response = requests.put(f"{API_URL}/productos/{id}", json=data)  # Endpoint para actualizar todo el producto
        if response.status_code == 200:
            flash("Producto actualizado correctamente.")
        else:
            flash("Error al actualizar producto.")

    except Exception as e:
        flash("Error al actualizar producto: " + str(e))

    return redirect(url_for('proveedor.proveedor_productos'))

@proveedor_bp.route('/pedidos')
def proveedor_pedidos():
    try:
        response = requests.get(f"{API_URL}/proveedores/")
        pedidos = response.json()

        print("📦 Pedidos del proveedor:")
        print(pedidos)

    except Exception as e:
        pedidos = []
        flash("Error al obtener pedidos: " + str(e))

    return render_template('templatesProveedor/Gestion_pedidos.html', pedidos=pedidos)

@proveedor_bp.route('/pedidos/agregar', methods=['POST'])
def agregar_pedido():
    cliente_id = request.form['cliente']
    fecha = request.form['fecha']
    estado = request.form['estado']
    total = request.form['total']

    data = {
        "cliente_id": int(cliente_id),
        "fecha": fecha,
        "estado": estado,
        "total": float(total)
    }

    try:
        response = requests.post(f"{API_URL}/proveedores/", json=data)
        if response.status_code == 200:
            flash("Pedido agregado exitosamente.")
        else:
            flash("Error al agregar el pedido.")
    except Exception as e:
        flash("Error al conectar con la API: " + str(e))

    return redirect(url_for('proveedor.proveedor_pedidos'))

@proveedor_bp.route('/promocion/enviar/<int:cliente_id>', methods=['POST'])
def enviar_promocion(cliente_id):
    promo_id = request.form['promo_id']
    response = requests.put(
        f'http://127.0.0.1:5002/clientes/promociones/{cliente_id}',
        json={"promo_id": int(promo_id)}
    )

    if response.status_code == 200:
        flash("Promoción enviada correctamente")
    else:
        flash("Error al enviar promoción", "danger")

    return redirect(url_for('proveedor.consultar_clientes'))

import requests
from flask import Blueprint, render_template

proveedor_bp = Blueprint('proveedor', __name__)

@proveedor_bp.route('/clientes')
def consultar_clientes():
    response = requests.get('http://127.0.0.1:5002/usuarios/')
    clientes = response.json()
    
    # Simulación de "frecuentes" con base en algún criterio (ej: ID par)
    frecuentes = [c for c in clientes if c["id"] % 2 == 0]

    # Simulación de promociones activas (en un caso real, sería otro endpoint)
    promociones = [
        {"id": 1, "titulo": "Descuento 20%", "valido_hasta": "2025-04-30", "activa": True},
        {"id": 2, "titulo": "2x1 en stickers", "valido_hasta": "2025-04-15", "activa": False}
    ]

    return render_template(
        'proveedor/clientes.html',
        clientes=clientes,
        frecuentes=frecuentes,
        promociones=promociones
    )

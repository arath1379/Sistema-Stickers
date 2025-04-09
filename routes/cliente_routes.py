import requests
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from datetime import datetime

cliente_bp = Blueprint('cliente', __name__, url_prefix='/cliente')

# Dirección base de la API
API_BASE_URL = 'http://localhost:5002'  # Cambia esto a la URL correcta de tu API

@cliente_bp.route('/dashboard')
def dashboard():
    if session.get('rol') != 'cliente':
        return "Acceso denegado", 403
    return render_template('templatesUser/cliente.html')

@cliente_bp.route('/catalogo')
def catalogo():
    try:
        # Hacer una solicitud GET al endpoint /productos/ de la API
        response = requests.get(f'{API_BASE_URL}/productos/')
        productos = response.json()  # Suponiendo que la respuesta es un JSON

        if response.status_code != 200:
            flash('Error al cargar los productos desde la API.', 'danger')
            productos = []  # Si ocurre un error, mostramos una lista vacía

    except requests.exceptions.RequestException as e:
        flash(f'Error de conexión con la API: {e}', 'danger')
        productos = []  # Si hay un error en la solicitud, mostramos una lista vacía

    return render_template('templatesUser/catalogo.html', productos=productos)

@cliente_bp.route('/carrito')
def carrito():
    productos = session.get('carrito', [])
    # Verificar y forzar que los precios sean flotantes
    for producto in productos:
        try:
            producto['precio'] = float(producto['precio'])
        except ValueError:
            flash("Hay un precio no válido en el carrito.")
            return redirect(url_for('cliente.catalogo'))
    
    total = sum(p['precio'] for p in productos)  # Sumar los precios convertidos
    return render_template('templatesUser/carrito.html', productos=productos, total=total)

@cliente_bp.route('/historial')
def historial():
    # Obtener el historial de compras desde la sesión
    pedidos = session.get('pedidos', [])
    return render_template('templatesUser/historial.html', pedidos=pedidos)

@cliente_bp.route('/pedidos')
def pedidos():
    try:
        # Hacer la solicitud GET para obtener los pedidos de todos los clientes
        response = requests.get(f'{API_BASE_URL}/clientes/')
        
        if response.status_code == 200:
            pedidos = response.json()  # Respuesta de la API con los pedidos
        else:
            flash('Error al cargar los pedidos desde la API.', 'danger')
            pedidos = []

    except requests.exceptions.RequestException as e:
        flash(f'Error de conexión con la API: {e}', 'danger')
        pedidos = []

    return render_template('templatesUser/pedidos.html', pedidos=pedidos)

@cliente_bp.route('/agregar-al-carrito', methods=['POST'])
def agregar_al_carrito():
    nombre = request.form.get('nombre')
    precio = request.form.get('precio')
    # Convertir el precio a float antes de agregarlo al carrito
    try:
        precio = float(precio)
    except ValueError:
        flash("El precio no es válido.")
        return redirect(url_for('cliente.catalogo'))
    
    imagen = "C:/Sistema-Stickers/static/images/default.jpg"

    carrito = session.get('carrito', [])
    carrito.append({"nombre": nombre, "precio": precio, "imagen": imagen, "id": len(carrito) + 1})
    session['carrito'] = carrito

    flash(f'{nombre} agregado al carrito.')
    return redirect(url_for('cliente.catalogo'))

@cliente_bp.route('/eliminar-del-carrito/<int:id>', methods=['POST'])
def eliminar_del_carrito(id):
    # Obtener el carrito de la sesión
    carrito = session.get('carrito', [])

    # Filtrar los productos que no coinciden con el id para eliminar el producto
    carrito = [producto for producto in carrito if producto['id'] != id]

    # Actualizar el carrito en la sesión
    session['carrito'] = carrito

    # Dar un mensaje de confirmación
    flash('Producto eliminado del carrito.')

    # Redirigir al carrito para que el usuario vea los cambios
    return redirect(url_for('cliente.carrito'))

@cliente_bp.route('/procesar-pago', methods=['POST'])
def procesar_pago():
    productos = session.get('carrito', [])
    total = sum(float(p['precio']) for p in productos)

    if productos:
        pedido = {
            'id': len(session.get('pedidos', [])) + 1,
            'producto': ', '.join([p['nombre'] for p in productos]),
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total': total,
            'estado': 'Completado',
            'imagen': productos[0]['imagen'] if productos else '',
        }

        pedidos = session.get('pedidos', [])
        pedidos.append(pedido)
        session['pedidos'] = pedidos

        session['carrito'] = []  # Limpiar el carrito después del pago

        flash(f'¡Pago realizado con éxito! Total: ${total:.2f}', 'success')

        return redirect(url_for('cliente.historial'))  # Redirige al historial
    else:
        flash('El carrito está vacío, no se pudo procesar el pago.', 'danger')
        return redirect(url_for('cliente.carrito'))

@cliente_bp.route('/realizar-pedido', methods=['POST'])
def realizar_pedido():
    # Obtener los productos del carrito de la sesión
    productos = session.get('carrito', [])
    
    if not productos:
        flash("Tu carrito está vacío. No se puede realizar un pedido.", "danger")
        return redirect(url_for('cliente.carrito'))

    # Crear un string con los productos
    productos_data = ", ".join([p['nombre'] for p in productos])
    
    # Calcular el total
    total = sum(p['precio'] for p in productos)

    # Obtener el cliente_id de la sesión (suponiendo que el ID del cliente está guardado en la sesión)
    cliente_id = session.get('cliente_id', 0)  # Cambia esto según cómo estés almacenando el ID del cliente

    if not cliente_id:
        flash("No se encontró el cliente_id en la sesión. Asegúrate de que has iniciado sesión.", "danger")
        return redirect(url_for('auth.login'))  # Redirigir al login si no hay cliente_id

    pedido_data = {
        'fecha_pedido': datetime.now().strftime('%Y-%m-%d'),  # Fecha del pedido
        'total': total,  # Total calculado
        'estado': 'pendiente',  # Estado del pedido
        'productos': productos_data,  # String con los productos
        'cliente_id': cliente_id,  # ID del cliente
    }

    try:
        # Enviar el pedido a la API para crear un nuevo pedido
        response = requests.post(f'{API_BASE_URL}/clientes/', json=pedido_data)

        if response.status_code == 201:  # Suponiendo que 201 es la respuesta para éxito
            flash("Pedido realizado con éxito.", "success")
            # Limpiar el carrito después de realizar el pedido
            session['carrito'] = []
        else:
            flash(f"Error al realizar el pedido: {response.text}", "danger")
    
    except requests.exceptions.RequestException as e:
        flash(f'Error de conexión con la API: {e}', "danger")

    # Redirigir a la página de pedidos para mostrar los cambios
    return redirect(url_for('cliente.pedidos'))

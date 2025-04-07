from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from models import Usuario, Producto, Pedido
from __init__ import db
from decorators import login_requerido
from datetime import datetime

main = Blueprint('main', __name__)
proveedor = Blueprint('proveedor', __name__, url_prefix='/proveedor')
inventario_bp = Blueprint('inventario', __name__, url_prefix='/proveedor/inventario')
pedidos = Blueprint('pedidos', __name__, url_prefix='/pedidos')

# ======================== DATOS SIMULADOS =========================
pedidos_simulados = []
clientes = []
promociones = []
chat_mensajes = []
notificaciones = 2  # Valor por defecto para las notificaciones
chat = []  # Chat para el admin

# ======================== AUTENTICACIÓN =========================

@main.route('/')
def inicio():
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        
        usuario = Usuario.query.filter_by(correo=correo, contrasena=contrasena).first()
        if usuario:
            session['usuario_id'] = usuario.id
            session['rol'] = usuario.rol
            session.permanent = True
            if usuario.rol == 'cliente':
                return redirect(url_for('main.dashboard_cliente'))
            elif usuario.rol == 'proveedor':
                return redirect(url_for('main.dashboard_proveedor'))
            elif usuario.rol == 'admin':
                return redirect(url_for('main.dashboard_admin'))
        else:
            flash('Credenciales incorrectas', 'login')
    
    return render_template('login.html')

@main.route('/registro', methods=['POST'])
def registro():
    nombre = request.form['nombre']
    correo = request.form['correo']
    contrasena = request.form['contrasena']
    rol = request.form['rol']

    if not nombre or not correo or not contrasena:
        flash('Todos los campos son obligatorios.', 'registro')
        return redirect(url_for('main.login'))

    existente = Usuario.query.filter_by(correo=correo).first()
    if existente:
        flash('El correo ya está registrado.', 'registro')
        return redirect(url_for('main.login'))

    nuevo_usuario = Usuario(nombre=nombre, correo=correo, contrasena=contrasena, rol=rol)
    db.session.add(nuevo_usuario)
    db.session.commit()
    flash('Registro exitoso. Ahora puedes iniciar sesión.', 'registro')
    return redirect(url_for('main.login'))

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))

# ======================== DASHBOARDS =========================

@main.route('/dashboard/cliente')
@login_requerido('cliente')
def dashboard_cliente():
    return render_template('templatesUser/cliente.html')

@main.route('/dashboard/proveedor')
@login_requerido('proveedor')
def dashboard_proveedor():
    return render_template('templatesProveedor/proveedor.html')

@main.route('/dashboard/admin')
@login_requerido('admin')
def dashboard_admin():
    return render_template('admin/admin.html')

# ======================== CLIENTE =========================

@main.route('/cliente/historial')
@login_requerido('cliente')
def historial_cliente():
    return render_template('cliente/historial.html')

@main.route('/cliente/pedidos')
@login_requerido('cliente')
def pedidos_cliente():
    return render_template('cliente/pedidos.html', pedidos=pedidos_simulados)

@main.route('/cliente/pedido/realizar', methods=['POST'])
@login_requerido('cliente')
def realizar_pedido():
    carrito = session.get('carrito', [])
    if not carrito:
        flash("Tu carrito está vacío", "error")
        return redirect(url_for('main.carrito_cliente'))

    total = sum(producto['precio'] for producto in carrito)
    cantidad = len(carrito)

    nuevo_pedido = {
        "id": 1000 + len(pedidos_simulados),
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "productos": f"{cantidad} producto{'s' if cantidad > 1 else ''}",
        "total": round(total, 2),
        "estado": "pendiente"
    }

    pedidos_simulados.insert(0, nuevo_pedido)
    session['carrito'] = []

    flash("¡Pedido realizado con éxito!", "success")
    return redirect(url_for('main.pedidos_cliente'))

@main.route('/cliente/perfil')
@login_requerido('cliente')
def perfil_cliente():
    usuario = Usuario.query.get(session['usuario_id'])
    return render_template('cliente/perfil.html', usuario=usuario)

@main.route('/cliente/perfil/editar', methods=['POST'])
@login_requerido('cliente')
def editar_perfil_cliente():
    usuario = Usuario.query.get(session['usuario_id'])

    nuevo_correo = request.form['correo']
    if usuario.correo != nuevo_correo:
        existente = Usuario.query.filter_by(correo=nuevo_correo).first()
        if existente:
            flash('Este correo ya está en uso.', 'perfil')
            return redirect(url_for('main.perfil_cliente'))

    usuario.nombre = request.form['nombre']
    usuario.correo = nuevo_correo
    usuario.direccion = request.form['direccion']

    db.session.commit()
    flash('Perfil actualizado con éxito', 'perfil')
    return redirect(url_for('main.perfil_cliente'))

@main.route('/cliente/catalogo')
@login_requerido('cliente')
def catalogo_cliente():
    productos = [
        {"id": 1, "nombre": "Sticker Anime Pack", "imagen": "images/sticker1.jpg", "precio": 15.00},
        {"id": 2, "nombre": "Sticker Superhéroes", "imagen": "images/sticker2.jpg", "precio": 12.00},
        {"id": 3, "nombre": "Sticker Retro", "imagen": "images/sticker3.jpg", "precio": 10.00}
    ]
    return render_template('cliente/catalogo.html', productos=productos)

@main.route('/cliente/catalogo/agregar', methods=['POST'])
@login_requerido('cliente')
def agregar_al_carrito():
    nombre = request.form.get('nombre')
    precio = request.form.get('precio')

    if not nombre or not precio:
        flash('Error al agregar al carrito', 'error')
        return redirect(url_for('main.catalogo_cliente'))

    producto = {'nombre': nombre, 'precio': float(precio)}
    carrito = session.get('carrito', [])
    carrito.append(producto)
    session['carrito'] = carrito

    flash(f'{nombre} agregado al carrito')
    return redirect(url_for('main.catalogo_cliente'))

@main.route('/cliente/carrito')
@login_requerido('cliente')
def carrito_cliente():
    productos = session.get('carrito', [])
    total = sum(p["precio"] for p in productos)
    return render_template('cliente/carrito.html', productos=productos, total=total)

@main.route('/cliente/carrito/vaciar')
@login_requerido('cliente')
def vaciar_carrito():
    session['carrito'] = []
    flash('Carrito vaciado')
    return redirect(url_for('main.carrito_cliente'))

@main.route('/procesar-pago', methods=['POST'])
@login_requerido('cliente')
def procesar_pago():
    session['carrito'] = []
    flash('Pago procesado con éxito')
    return redirect(url_for('main.historial_cliente'))

# ======================== PROVEEDOR =========================

@proveedor.route("/clientes")
@login_requerido('proveedor')
def clientes_view():
    frecuentes = [c for c in clientes if c.get("frecuente")]
    return render_template("proveedor/clientes.html", clientes=clientes, frecuentes=frecuentes, promociones=promociones)

@proveedor.route("/cliente/<int:cliente_id>")
@login_requerido('proveedor')
def ver_cliente(cliente_id):
    return f"Ver cliente {cliente_id}"

@proveedor.route("/promocion/<promo_id>")
@login_requerido('proveedor')
def ver_promocion(promo_id):
    return f"Ver promoción {promo_id}"

@proveedor.route("/promocion/enviar/<promo_id>")
@login_requerido('proveedor')
def enviar_promocion(promo_id):
    return f"Enviar promoción {promo_id}"

@proveedor.route("/pedidos")
@login_requerido('proveedor')
def pedidos_view():
    return render_template("proveedor/pedidos.html")

@proveedor.route('/enviar_mensaje', methods=['POST'])
@login_requerido('proveedor')
def enviar_mensaje():
    mensaje = request.form.get('mensaje')
    if mensaje:
        chat_mensajes.append({"usuario": "Tú", "texto": mensaje})
    return redirect(url_for('main.dashboard_proveedor'))

# ======================== INVENTARIO =========================

@inventario_bp.route('/', methods=['GET', 'POST'])
@login_requerido('proveedor')
def inventario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = float(request.form['precio'])
        cantidad = int(request.form['cantidad'])

        nuevo_producto = Producto(nombre=nombre, categoria=categoria, precio=precio, cantidad=cantidad)
        db.session.add(nuevo_producto)
        db.session.commit()

        flash('Producto agregado exitosamente')
        return redirect(url_for('inventario.inventario'))

    productos = Producto.query.all()
    return render_template('proveedor/inventario.html', productos=productos)

@inventario_bp.route('/editar/<int:id>', methods=['POST'])
@login_requerido('proveedor')
def editar_producto(id):
    producto = Producto.query.get_or_404(id)

    producto.nombre = request.form['nombre']
    producto.categoria = request.form['categoria']
    producto.precio = float(request.form['precio'])
    producto.cantidad = int(request.form['cantidad'])

    db.session.commit()
    flash('Producto actualizado correctamente')
    return redirect(url_for('inventario.inventario'))

@inventario_bp.route('/eliminar/<int:id>')
@login_requerido('proveedor')
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado correctamente')
    return redirect(url_for('inventario.inventario'))

# ======================== PEDIDOS ADMIN =========================

@pedidos.route('/')
@login_requerido('admin')
def index():
    pedidos_lista = Pedido.query.all()
    return render_template('admin/pedidos.html', pedidos=pedidos_lista)

@pedidos.route('/agregar', methods=['POST'])
@login_requerido('admin')
def agregar_pedido():
    cliente_id = request.form['cliente']
    fecha = request.form['fecha']
    estado = request.form['estado']
    total = request.form['total']
    
    nuevo_pedido = Pedido(
        cliente_id=cliente_id,
        fecha=datetime.strptime(fecha, '%Y-%m-%d').date(),
        estado=estado,
        total=float(total)
    )
    
    try:
        db.session.add(nuevo_pedido)
        db.session.commit()
        flash('Pedido agregado exitosamente')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al agregar pedido: {str(e)}')
    
    return redirect(url_for('pedidos.index'))

@pedidos.route('/editar/<int:id>', methods=['POST'])
@login_requerido('admin')
def editar_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    
    pedido.cliente_id = request.form['cliente']
    pedido.fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()
    pedido.estado = request.form['estado']
    pedido.total = float(request.form['total'])
    
    try:
        db.session.commit()
        flash('Pedido actualizado exitosamente')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar pedido: {str(e)}')
    
    return redirect(url_for('pedidos.index'))

@pedidos.route('/eliminar/<int:id>')
@login_requerido('admin')
def eliminar_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    
    try:
        db.session.delete(pedido)
        db.session.commit()
        flash('Pedido eliminado exitosamente')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar pedido: {str(e)}')
    
    return redirect(url_for('pedidos.index'))

# ======================== ADMIN (MÓDULO PRINCIPAL) =========================

# Estas rutas deben estar definidas dentro de un blueprint para admin
# Si no existe un blueprint específico, las agregaremos al main

@main.route('/admin/dashboard')
def admin_dashboard():
    return render_template("admin_dashboard.html", mensajes_chat=chat, notificaciones=notificaciones)

@main.route('/admin/gestion_roles')
def gestion_roles():
    return "Gestión de Roles (en desarrollo)"

@main.route('/admin/reportes')
def reportes():
    return "Reportes y Estadísticas (en desarrollo)"

@main.route('/admin/clientes')
def clientes_admin():
    return "Gestión de Clientes (en desarrollo)"

@main.route('/admin/proveedores')
def proveedores():
    return "Gestión de Proveedores (en desarrollo)"

@main.route('/admin/ver_notificaciones')
def ver_notificaciones():
    global notificaciones
    notificaciones = 0
    return redirect(url_for('main.admin_dashboard'))

@main.route('/admin/enviar_mensaje', methods=["POST"])
def admin_enviar_mensaje():
    mensaje = request.form.get("mensaje", "").strip()
    if mensaje:
        chat.append({"autor": "Tú", "contenido": mensaje})
    return redirect(url_for('main.admin_dashboard'))

# ======================== RUTAS PARA GESTIÓN DE ROLES =========================

@main.route("/admin/roles")
def roles():
    # Simulamos obtener roles de la base de datos
    roles = [{"id": 1, "nombre": "Admin", "descripcion": "Acceso total"}, 
             {"id": 2, "nombre": "Cliente", "descripcion": "Usuario regular"}, 
             {"id": 3, "nombre": "Proveedor", "descripcion": "Gestor de inventario"}]
    return render_template("admin/gestion_roles.html", roles=roles)

@main.route("/admin/roles/agregar", methods=["POST"])
def agregar_rol():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    # Aquí iría la lógica para agregar el rol a la base de datos
    flash('Rol agregado exitosamente')
    return redirect(url_for('main.roles'))

@main.route("/admin/roles/eliminar/<int:rol_id>")
def eliminar_rol(rol_id):
    # Aquí iría la lógica para eliminar el rol de la base de datos
    flash('Rol eliminado exitosamente')
    return redirect(url_for('main.roles'))

@main.route("/admin/roles/editar/<int:rol_id>")
def editar_rol(rol_id):
    # Simulamos obtener un rol específico de la base de datos
    rol = {"id": rol_id, "nombre": "Rol ejemplo", "descripcion": "Descripción del rol"}
    return render_template("admin/editar_rol.html", rol=rol)

@main.route("/admin/roles/actualizar/<int:rol_id>", methods=["POST"])
def actualizar_rol(rol_id):
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    # Aquí iría la lógica para actualizar el rol en la base de datos
    flash('Rol actualizado exitosamente')
    return redirect(url_for('main.roles'))
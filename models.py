from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL, Text, Boolean, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from __init__ import db


class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    correo = Column(String(100), unique=True)
    contrasena = Column(String(100))
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    rol = Column(String(50))  # Añadir esta línea

    roles = relationship("UsuarioRol", back_populates="usuario")


class Cliente(db.Model):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    telefono = Column(String(20))
    direccion = Column(Text)
    
    usuario = relationship("Usuario")


class Proveedor(db.Model):
    __tablename__ = "proveedores"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    correo = Column(String(100))
    telefono = Column(String(20))
    direccion = Column(String(255))
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    
    productos = relationship("Producto", back_populates="proveedor")


class Producto(db.Model):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    descripcion = Column(Text)
    precio = Column(DECIMAL(10, 2))
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"), nullable=True) 
    stock = Column(Integer)

    proveedor = relationship("Proveedor", back_populates="productos")
    inventario = relationship("Inventario", back_populates="producto")
    detalles = relationship("DetallePedido", back_populates="producto")


class Pedido(db.Model):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha_pedido = Column(DateTime, default=datetime.utcnow)
    estado = Column(String(50))

    usuario = relationship("Usuario")
    detalles = relationship("DetallePedido", back_populates="pedido")
    ventas = relationship("Venta", back_populates="pedido")


class Venta(db.Model):
    __tablename__ = "ventas"
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    total = Column(Numeric(10, 2))
    fecha_venta = Column(DateTime, default=datetime.utcnow)

    pedido = relationship("Pedido", back_populates="ventas")


class DetallePedido(db.Model):
    __tablename__ = "detalles_pedido"
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer)
    precio_unitario = Column(DECIMAL(10, 2))

    pedido = relationship("Pedido", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles")


class Inventario(db.Model):
    __tablename__ = "inventario"
    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow)

    producto = relationship("Producto", back_populates="inventario")


class Notificacion(db.Model):
    __tablename__ = "notificaciones"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    mensaje = Column(Text)
    leida = Column(Boolean, default=False)
    fecha_envio = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario")


class Reporte(db.Model):
    __tablename__ = "reportes"
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50))
    datos = Column(Text)


class Rol(db.Model):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    descripcion = Column(Text)
    
    permisos = relationship("RolPermiso", back_populates="rol")
    usuarios = relationship("UsuarioRol", back_populates="rol")


class Permiso(db.Model):
    __tablename__ = "permisos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    descripcion = Column(Text)
    
    roles = relationship("RolPermiso", back_populates="permiso")


class RolPermiso(db.Model):
    __tablename__ = "roles_permisos"
    id = Column(Integer, primary_key=True, index=True)
    rol_id = Column(Integer, ForeignKey("roles.id"))
    permiso_id = Column(Integer, ForeignKey("permisos.id"))
    
    rol = relationship("Rol", back_populates="permisos")
    permiso = relationship("Permiso", back_populates="roles")


class UsuarioRol(db.Model):
    __tablename__ = "usuario_roles"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    rol_id = Column(Integer, ForeignKey("roles.id"))

    usuario = relationship("Usuario", back_populates="roles")
    rol = relationship("Rol", back_populates="usuarios")
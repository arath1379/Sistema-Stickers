from flask import Flask
from routes.auth_routes import auth_bp
from routes.cliente_routes import cliente_bp
from routes.proveedor_routes import proveedor_bp
from routes.admin_routes import admin_bp

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Cambia esto en producción

# Registro de rutas
app.register_blueprint(auth_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(proveedor_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run(debug=True, port=8002)

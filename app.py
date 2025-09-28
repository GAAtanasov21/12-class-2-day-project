from flask import Flask, render_template
from controllers.auth_controller import auth_bp
from controllers.catalog_controller import catalog_bp
from controllers.cart_controller import cart_bp
from controllers.admin_controller import admin_bp
from services.auth_service import init_sample_users
from services.catalog_service import init_sample_products
from controllers.order_controller import order_bp
app = Flask(__name__)
app.secret_key = "supersecret"

# Initialize data
init_sample_users()
init_sample_products()

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(catalog_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(order_bp)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

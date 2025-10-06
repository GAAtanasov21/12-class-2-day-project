from flask import Flask, render_template
from controllers.auth_controller import auth_bp
from controllers.catalog_controller import catalog_bp
from controllers.cart_controller import cart_bp
from controllers.order_controller import order_bp
from controllers.admin_controller import admin_bp
from services.models import db
from services.init_data import init_sample_data

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'supersecret-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shoestore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(catalog_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(order_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def index():
    return render_template('index.html')

# Create database tables and initialize sample data
with app.app_context():
    db.create_all()
    init_sample_data()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
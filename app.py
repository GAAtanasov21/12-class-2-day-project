from flask import Flask, render_template
from controllers.auth_controller import auth_bp
from controllers.admin_controller import admin_bp
app = Flask(__name__)
app.secret_key = "dev-secret-key"
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


if __name__ == '__main__':
    app.run()

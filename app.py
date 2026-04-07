from flask import Flask, render_template, redirect, url_for, request, session
from database import db
from models import User

from routes.auth import auth_bp
from routes.records import records_bp
from routes.users import users_bp

app = Flask(__name__)
app.secret_key = "secret123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register routes
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(records_bp, url_prefix='/records')
app.register_blueprint(users_bp, url_prefix='/users')


@app.route('/')
def home():
    return redirect(url_for('login_page'))


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['role'] = user.role
            return redirect(url_for('dashboard'))

        return "Invalid credentials"

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'role' not in session:
        return redirect(url_for('login_page'))
    return render_template('dashboard.html', role=session['role'])


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
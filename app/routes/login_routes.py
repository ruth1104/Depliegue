from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import login_user, logout_user, login_required
from app import db
from app.models.user import User
from app.models.apprentice import Apprentices
from app.models.instrutor import Instructors
from app.models.wachiman import Wachiman
from functools import wraps
from flask_login import current_user


bp = Blueprint('auth', __name__)

@bp.route('/indexUser')
def index():
    users = User.query.all()
    return render_template('login/index.html', users=users)

@bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["nameUser"]
        password = request.form["passwordUser"]

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)

            if user.rol == "Aprendiz":
                return redirect(url_for('apprentice.index', id=user.idUser))
            elif user.rol == "Celador":
                return redirect(url_for("wachiman.index", id=user.idUser))
            elif user.rol == "Instructor":
                return redirect(url_for("intructor.index", id=user.idUser))

    return render_template("login/login.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/add', methods=['GET', 'POST'])    
def add():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        rol = request.form['rol']
        
        # Encriptar la contraseña
       # hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=password, rol=rol)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('auth.index'))
    return render_template('login/add.html')

@bp.route('/user/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        user.username = request.form['username']
        
        new_password = request.form['password']
        if new_password:
            user.password = request.form['password']

        user.rol = request.form['rol']
        db.session.commit()
        
        return redirect(url_for('auth.index'))

    return render_template('login/edit.html', user=user)

@bp.route('/user/delete/<int:id>')
def delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('auth.index'))

def requiere_rol(roles_permitidos):
    def decorador(f):
        @wraps(f)  # Esto preserva el __name__ y evita conflictos
        def funcion_decorada(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Debes iniciar sesión.', 'danger')
                return redirect(url_for('auth.login'))

            if current_user.rol not in roles_permitidos:
                flash('Acceso denegado.', 'danger')
                return redirect(url_for('auth.index'))

            return f(*args, **kwargs)
        return funcion_decorada
    return decorador

@bp.route("/apprentice")
@login_required
@requiere_rol(["Aprendiz"])
def apprentice_dashboard():
    print("Rol actual:", current_user.rol)
    return render_template("apprentice/index.html")

@bp.route("/equipment")
@login_required
@requiere_rol(["Aprendiz", "Instructor", "Celador"])
def equipmet_dashboard():
    return render_template("equipment/index.html")

@bp.route("/intructor")
@login_required
@requiere_rol(["Instructor", "Celador"])
def instructor_dashboard():
    return render_template("instructor/index.html")

@bp.route("/wachiman")
@login_required
@requiere_rol(["Celador"])
def wachiman_dashboard():
    return render_template("Wachiman/index.html")
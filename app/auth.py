from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User
import functools

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Для доступа к данной странице необходимо пройти процедуру аутентификации.'
    login_manager.login_message_category = 'warning'
    login_manager.user_loader(load_user)
    login_manager.init_app(app)

def load_user(user_id):
    user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar()
    return user

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        if login and password:
            user = db.session.execute(db.select(User).filter_by(login=login)).scalar()
            if user and user.check_password(password):
                login_user(user)
                flash('Вы успешно аутентифицированы.', 'success')
                next = request.args.get('next')
                return redirect(next or url_for('index'))
        flash('Введены неверные логин и/или пароль.', 'danger')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

def check_rights(action):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            book_id = kwargs.get('book_id')
            if not current_user.can(action, book_id=book_id):
                flash('У вас недостаточно прав для доступа к данной странице.', 'danger')
                return redirect(url_for('index'))
            return function(*args, **kwargs)
        return wrapper
    return decorator



def check_rights_collection(action):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            user_id = kwargs.get('user_id')
            if not current_user.can_coll(action, user_id=user_id):
                flash('У вас недостаточно прав для доступа к данной странице.', 'danger')
                return redirect(url_for('index'))
            return function(*args, **kwargs)
        return wrapper
    return decorator


def check_rights_to_coll(action):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            collection_id = kwargs.get('collection_id')
            if not current_user.can_collection(action, collection_id=collection_id):
                flash('У вас недостаточно прав для доступа к данной странице.', 'danger')
                return redirect(url_for('index'))
            return function(*args, **kwargs)
        return wrapper
    return decorator





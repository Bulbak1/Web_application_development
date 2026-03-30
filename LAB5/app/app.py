import re
import random
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from faker import Faker

fake = Faker()

app = Flask(__name__)
application = app
app.secret_key = 'supersecretkey123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа к этой странице необходимо пройти процедуру аутентификации.'
login_manager.login_message_category = 'warning'

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    users = db.relationship('User', back_populates='role')


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(100), nullable=True)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    role = db.relationship('Role', back_populates='users')

    def get_full_name(self):
        parts = [self.last_name, self.first_name, self.middle_name]
        return ' '.join(p for p in parts if p)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

# 5 lab

class VisitLog(db.Model):
    __tablename__ = 'visit_logs'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    user = db.relationship('User', backref='visit_logs')

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()

def init_db():
    db.create_all()
    if not Role.query.first():
        db.session.add_all([
            Role(name='Администратор', description='Полный доступ к системе'),
            Role(name='Пользователь', description='Стандартный доступ'),
        ])
        db.session.commit()
    if not User.query.first():
        admin_role = Role.query.filter_by(name='Администратор').first()
        admin = User(
            login='admin',
            first_name='Админ',
            last_name='Главный',
            role_id=admin_role.id if admin_role else None
        )
        admin.set_password('Qwerty123!')
        db.session.add(admin)
        db.session.commit()

# 5 lab
def check_rights(action):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('У вас недостаточно прав для доступа к данной странице.', 'warning')
                return redirect(url_for('index'))

            role_name = current_user.role.name if current_user.role else None
            allowed = False

            if role_name == 'Администратор':
                allowed = True
            elif role_name == 'Пользователь':
                if action in ('edit_users', 'view_profile'):
                    user_id = kwargs.get('user_id')
                    allowed = (user_id == current_user.id)
                elif action == 'view_logs':
                    allowed = True

            if not allowed:
                flash('У вас недостаточно прав для доступа к данной странице.', 'warning')
                return redirect(url_for('index'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.before_request
def log_visit():
    if not request.path.startswith('/static/'):
        try:
            log_entry = VisitLog(
                path=request.path,
                user_id=current_user.id if current_user.is_authenticated else None
            )
            db.session.add(log_entry)
            db.session.commit()
        except Exception:
            db.session.rollback()
            
# ===== Посты (из ЛР1) =====

images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']


def generate_comments(replies=True):
    comments = []
    for i in range(random.randint(1, 3)):
        comment = {'author': fake.name(), 'text': fake.text()}
        if replies:
            comment['replies'] = generate_comments(replies=False)
        comments.append(comment)
    return comments


def generate_post(i):
    return {
        'title': 'Заголовок поста',
        'text': fake.paragraph(nb_sentences=100),
        'author': fake.name(),
        'date': fake.date_time_between(start_date='-2y', end_date='now'),
        'image_id': f'{images_ids[i]}.jpg',
        'comments': generate_comments()
    }


posts_list = sorted([generate_post(i) for i in range(5)], key=lambda p: p['date'], reverse=True)

# ===== Валидация =====

def validate_login(login):
    errors = []
    if not login:
        errors.append('Поле не может быть пустым.')
    elif len(login) < 5:
        errors.append('Логин должен содержать не менее 5 символов.')
    elif not re.match(r'^[a-zA-Z0-9]+$', login):
        errors.append('Логин должен состоять только из латинских букв и цифр.')
    return errors


def validate_password(password):
    errors = []
    if not password:
        errors.append('Поле не может быть пустым.')
        return errors
    if len(password) < 8:
        errors.append('Пароль должен содержать не менее 8 символов.')
    if len(password) > 128:
        errors.append('Пароль не должен превышать 128 символов.')
    if not re.search(r'[A-ZА-ЯЁ]', password):
        errors.append('Пароль должен содержать хотя бы одну заглавную букву.')
    if not re.search(r'[a-zа-яё]', password):
        errors.append('Пароль должен содержать хотя бы одну строчную букву.')
    if not re.search(r'\d', password):
        errors.append('Пароль должен содержать хотя бы одну цифру.')
    if ' ' in password:
        errors.append('Пароль не должен содержать пробелы.')

    allowed_special = set('~!?@#$%^&*_-+()[]{}><\\/|"\'.,;:')
    for ch in password:
        if ch.isalpha() and not re.match(r'[a-zA-Zа-яёА-ЯЁ]', ch):
            errors.append('Пароль содержит буквы недопустимого алфавита.')
            break
        if ch.isdigit() and not re.match(r'[0-9]', ch):
            errors.append('Пароль должен содержать только арабские цифры.')
            break
        if not (ch.isalpha() or ch.isdigit() or ch in allowed_special):
            errors.append('Пароль содержит недопустимые символы.')
            break
    return errors


def validate_phone(phone):
    if re.search(r'[^\d\s\(\)\-\.\+]', phone):
        return None, 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.'
    digits = re.sub(r'\D', '', phone)
    stripped = phone.strip()
    starts_with_plus7 = stripped.startswith('+7')
    starts_with_8 = stripped.startswith('8')
    expected = 11 if (starts_with_plus7 or starts_with_8) else 10
    if len(digits) != expected:
        return None, 'Недопустимый ввод. Неверное количество цифр.'
    d = digits[1:] if len(digits) == 11 else digits
    formatted = f'8-{d[0:3]}-{d[3:6]}-{d[6:8]}-{d[8:10]}'
    return formatted, None


# ===== Маршруты ЛР1-3 =====

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts')
def posts():
    return render_template('posts.html', title='Посты', posts=posts_list)


@app.route('/posts/<int:index>')
def post(index):
    p = posts_list[index]
    return render_template('post.html', title=p['title'], post=p)


@app.route('/about')
def about():
    return render_template('about.html', title='Об авторе')


@app.route('/request-info')
def request_info():
    return render_template('request_info.html', title='Параметры запроса')


@app.route('/counter')
def counter():
    session['visits'] = session.get('visits', 0) + 1
    return render_template('counter.html', title='Счётчик посещений', visits=session['visits'])


@app.route('/phone', methods=['GET', 'POST'])
def phone():
    phone_input = ''
    formatted = None
    error = None
    if request.method == 'POST':
        phone_input = request.form.get('phone', '')
        formatted, error = validate_phone(phone_input)
    return render_template('phone.html', title='Проверка телефона',
                           phone_input=phone_input, formatted=formatted, error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'
        user = User.query.filter_by(login=username).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash('Вы успешно вошли в систему!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        flash('Неверный логин или пароль.', 'danger')
    return render_template('login.html', title='Авторизация')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('index'))


@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html', title='Секретная страница')


# ===== Маршруты ЛР4 =====

@app.route('/users')
def users_list():
    users = User.query.all()
    return render_template('users.html', title='Пользователи', users=users)


@app.route('/users/<int:user_id>')
@check_rights('view_profile')
def user_view(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    return render_template('user_view.html', title=f'Пользователь: {user.login}', user=user)


@app.route('/users/create', methods=['GET', 'POST'])
@check_rights('create_users')
def user_create():
    roles = Role.query.all()
    errors = {}
    form_data = {}

    if request.method == 'POST':
        login_val = request.form.get('login', '').strip()
        password = request.form.get('password', '')
        last_name = request.form.get('last_name', '').strip()
        first_name = request.form.get('first_name', '').strip()
        middle_name = request.form.get('middle_name', '').strip()
        role_id = request.form.get('role_id') or None

        form_data = {
            'login': login_val, 'last_name': last_name, 
            #'password': password,
            'first_name': first_name, 'middle_name': middle_name,
            'role_id': role_id,
        }

        login_errors = validate_login(login_val)
        if login_errors:
            errors['login'] = login_errors
        elif User.query.filter_by(login=login_val).first():
            errors['login'] = ['Пользователь с таким логином уже существует.']

        password_errors = validate_password(password)
        if password_errors:
            errors['password'] = password_errors

        if not last_name:
            errors['last_name'] = ['Поле не может быть пустым.']
        if not first_name:
            errors['first_name'] = ['Поле не может быть пустым.']

        if not errors:
            try:
                new_user = User(
                    login=login_val,
                    first_name=first_name,
                    last_name=last_name or None,
                    middle_name=middle_name or None,
                    role_id=int(role_id) if role_id else None
                )
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                flash('Пользователь успешно создан!', 'success')
                return redirect(url_for('users_list'))
            except Exception as e:
                db.session.rollback()
                flash(f'Ошибка при сохранении: {e}', 'danger')

    return render_template('user_create.html', title='Создать пользователя',
                           roles=roles, errors=errors, form_data=form_data)


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@check_rights('edit_users')
def user_edit(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    roles = Role.query.all()
    errors = {}
    is_admin = current_user.role and current_user.role.name == 'Администратор'

    if request.method == 'POST':
        last_name = request.form.get('last_name', '').strip()
        first_name = request.form.get('first_name', '').strip()
        middle_name = request.form.get('middle_name', '').strip()
        role_id = request.form.get('role_id') or None

        form_data = {
            'last_name': last_name, 'first_name': first_name,
            'middle_name': middle_name, 'role_id': role_id,
        }

        if not last_name:
            errors['last_name'] = ['Поле не может быть пустым.']
        if not first_name:
            errors['first_name'] = ['Поле не может быть пустым.']

        if not errors:
            try:
                user.last_name = last_name or None
                user.first_name = first_name
                user.middle_name = middle_name or None
                if is_admin:
                    user.role_id = int(role_id) if role_id else None
                db.session.commit()
                flash('Данные пользователя обновлены!', 'success')
                return redirect(url_for('users_list'))
            except Exception as e:
                db.session.rollback()
                flash(f'Ошибка при сохранении: {e}', 'danger')
    else:
        form_data = {
            'last_name': user.last_name or '',
            'first_name': user.first_name or '',
            'middle_name': user.middle_name or '',
            'role_id': user.role_id,
        }

    return render_template('user_edit.html', title='Редактировать пользователя',
                       user=user, roles=roles, errors=errors, form_data=form_data,
                       disable_role=not is_admin)


@app.route('/users/<int:user_id>/delete', methods=['POST'])
@check_rights('delete_users')
def user_delete(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()

    if user.id == current_user.id:
        flash('Невозможно удалить собственную учётную запись.', 'danger')
        return redirect(url_for('users_list'))
    
    if user.role and user.role.name == 'Администратор' and User.query.join(Role).filter(Role.name == 'Администратор').count() == 1:
        flash('Невозможно удалить единственного администратора.', 'danger')
        return redirect(url_for('users_list'))
    try:
        db.session.delete(user)
        db.session.commit()
        flash('Пользователь удалён.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении: {e}', 'danger')
    return redirect(url_for('users_list'))


@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    errors = {}
    if request.method == 'POST':
        old_password = request.form.get('old_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not current_user.check_password(old_password):
            errors['old_password'] = ['Неверный текущий пароль.']

        new_pwd_errors = validate_password(new_password)
        if new_pwd_errors:
            errors['new_password'] = new_pwd_errors

        if new_password and not new_pwd_errors and confirm_password != new_password:
            errors['confirm_password'] = ['Пароли не совпадают.']

        if not errors:
            try:
                current_user.set_password(new_password)
                db.session.commit()
                flash('Пароль успешно изменён!', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                flash(f'Ошибка: {e}', 'danger')

    return render_template('change_password.html', title='Смена пароля', errors=errors)


# ===== Инициализация БД =====
from visit_logs import visit_logs_bp
app.register_blueprint(visit_logs_bp)

with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True)
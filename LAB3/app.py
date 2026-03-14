import random
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from faker import Faker
import re

fake = Faker()

app = Flask(__name__)
application = app
app.secret_key = 'supersecretkey123'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа к этой странице необходимо пройти процедуру аутентификации.'
login_manager.login_message_category = 'warning'

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

USERS = {
    'user': User(id=1, username='user', password='qwerty')
}

@login_manager.user_loader
def load_user(user_id):
    for u in USERS.values():
        if str(u.id) == str(user_id):
            return u
    return None

images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']

def generate_comments(replies=True):
    comments = []
    for i in range(random.randint(1, 3)):
        comment = { 'author': fake.name(), 'text': fake.text() }
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
    
    if len(digits) == 11:
        d = digits[1:]
    else:
        d = digits
    formatted = f'8-{d[0:3]}-{d[3:6]}-{d[6:8]}-{d[8:10]}'
    return formatted, None

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'
        user = USERS.get(username)
        if user and user.password == password:
            login_user(user, remember=remember)
            flash('Вы успешно вошли в систему!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
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

if __name__ == '__main__':
    app.run(debug=True)
import secrets
import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.models import User, Jobs, Department, Category
from forms.user import RegisterForm
from forms.job import JobForm
from forms.department import DepartmentForm
from forms.auth import LoginForm
from forms.category import CategoryForm
from urllib.parse import urlparse

app = Flask(__name__)

# Настройка секретного ключа
FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"
if FLASK_DEBUG:
    app.config['SECRET_KEY'] = secrets.token_hex(32)
    print(f"🔧 [DEV MODE] SECRET_KEY: {app.config['SECRET_KEY'][:8]}...")
else:
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
    if not app.config['SECRET_KEY']:
        raise RuntimeError("Секретный ключ не задан! Установите переменную окружения FLASK_SECRET_KEY")

# Инициализация Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Пожалуйста, войдите в систему для доступа к этой странице"
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)  # Используем современный метод Session.get()

# Инициализация базы данных (ТОЛЬКО ОДИН РАЗ)
DB_FILE = "mars_explorer.db"
db_session.global_init(DB_FILE)

# Создание начальных данных (выполняется только один раз при запуске)
def create_initial_data():
    db_sess = db_session.create_session()
    
    # Проверяем, есть ли уже пользователи в базе
    if db_sess.query(User).count() == 0:
        print("Создание начальных данных...")
        
        # Создание капитана
        captain = User(
            surname="Scott",
            name="Ridley",
            age=21,
            position="captain",
            speciality="research engineer",
            address="module_1",
            email="scott_chief@mars.org"
        )
        captain.set_password("captain123")
        db_sess.add(captain)
        db_sess.commit()  # Коммитим сразу после первого пользователя
        
        # Получаем ID капитана после коммита
        captain_id = captain.id
        
        # Создание дополнительных пользователей
        users = [
            User(surname="Ivanov", name="Petr", age=25, position="engineer", speciality="robotics", address="module_1", email="ivanov@marss.org"),
            User(surname="Petrov", name="Alexey", age=28, position="geologist", speciality="mineralogy", address="module_2", email="petrov@marss.org"),
            User(surname="Sidorov", name="Nikolay", age=32, position="chief engineer", speciality="life support", address="module_1", email="sidorov@marss.org"),
            User(surname="Kuznetsov", name="Dmitry", age=22, position="biologist", speciality="ecology", address="module_3", email="kuznetsov@marss.org"),
            User(surname="Smirnov", name="Mikhail", age=27, position="middle engineer", speciality="energy systems", address="module_1", email="smirnov@marss.org")
        ]
        
        for user in users:
            user.set_password("colonist123")
            db_sess.add(user)
        db_sess.commit()
        
        # Создание категорий
        categories = [
            Category(name="Construction", description="Строительные работы"),
            Category(name="Research", description="Научные исследования"),
            Category(name="Maintenance", description="Техническое обслуживание"),
            Category(name="Exploration", description="Исследование территории")
        ]
        
        for category in categories:
            db_sess.add(category)
        db_sess.commit()
        
        # Получаем ID первой категории
        construction_category = db_sess.query(Category).filter_by(name="Construction").first()
        construction_id = construction_category.id if construction_category else None
        
        # Создание департаментов
        departments = [
            Department(title="Geological Exploration", chief=captain_id, members="1,2,3", email="geology@marss.org"),
            Department(title="Life Support Systems", chief=3, members="3,4,5", email="life-support@marss.org")
        ]
        db_sess.add_all(departments)
        db_sess.commit()
        
        # Создание первой работы (используем ID после коммита)
        job = Jobs(
            team_leader=captain_id,
            job="deployment of residential modules 1 and 2",
            work_size=15,
            collaborators="2, 3",
            is_finished=False
        )
        
        # Добавление категории к работе
        if construction_category:
            job.categories.append(construction_category)
        
        db_sess.add(job)
        db_sess.commit()
        
        print("✅ Начальные данные успешно созданы!")
    else:
        print("ℹ️ База данных уже содержит данные, пропускаем инициализацию")

# Главная страница
@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    
    # Добавляем дополнительную информацию для каждой работы
    for job in jobs:
        job.team_leader_obj = db_sess.get(User, job.team_leader)
        job.categories_list = ", ".join([category.name for category in job.categories]) if job.categories else "Без категории"
    
    return render_template("index.html", jobs=jobs, current_user=current_user)

# Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы успешно вошли в систему!', 'success')
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        else:
            flash('Неправильный email или пароль', 'danger')
    return render_template('login.html', form=form)

# Выход из системы
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы', 'info')
    return redirect(url_for('index'))

# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            flash('Пользователь с таким email уже существует', 'danger')
            return render_template('register.html', form=form)
        
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        
        flash('Регистрация прошла успешно! Теперь вы можете войти в систему.', 'success')
        return redirect('/login')
    
    return render_template('register.html', form=form, title='Регистрация')

# Создание работы
@app.route('/create_job', methods=['GET', 'POST'])
@login_required
def create_job():
    form = JobForm()
    db_sess = db_session.create_session()
    categories = db_sess.query(Category).all()
    form.categories.choices = [(category.id, category.name) for category in categories]
    
    if form.validate_on_submit():
        job = Jobs(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        
        # Добавление категорий
        selected_categories = db_sess.query(Category).filter(Category.id.in_(form.categories.data)).all()
        for category in selected_categories:
            job.categories.append(category)
        
        db_sess.add(job)
        db_sess.commit()
        
        flash('Работа успешно добавлена!', 'success')
        return redirect('/')
    
    return render_template('create_job.html', form=form, title='Создание работы')

# Редактирование работы
@app.route('/edit_job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(id)
    
    if not job:
        flash('Работа не найдена', 'danger')
        return redirect('/')
    
    # Проверка прав доступа: только автор или капитан (id=1)
    if current_user.id != job.team_leader and current_user.id != 1:
        flash('У вас нет прав для редактирования этой работы', 'danger')
        return redirect('/')
    
    form = JobForm()
    categories = db_sess.query(Category).all()
    form.categories.choices = [(category.id, category.name) for category in categories]
    
    if request.method == "GET":
        form.team_leader.data = job.team_leader
        form.job.data = job.job
        form.work_size.data = job.work_size
        form.collaborators.data = job.collaborators
        form.is_finished.data = job.is_finished
        form.categories.data = [category.id for category in job.categories]
    
    if form.validate_on_submit():
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        
        # Обновление категорий
        job.categories.clear()
        selected_categories = db_sess.query(Category).filter(Category.id.in_(form.categories.data)).all()
        for category in selected_categories:
            job.categories.append(category)
        
        db_sess.commit()
        flash('Работа успешно обновлена!', 'success')
        return redirect('/')
    
    return render_template('create_job.html', form=form, title='Редактирование работы')

# Удаление работы
@app.route('/delete_job/<int:id>', methods=['POST'])
@login_required
def delete_job(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(id)
    
    if not job:
        flash('Работа не найдена', 'danger')
        return redirect('/')
    
    # Проверка прав доступа: только автор или капитан (id=1)
    if current_user.id != job.team_leader and current_user.id != 1:
        flash('У вас нет прав для удаления этой работы', 'danger')
        return redirect('/')
    
    db_sess.delete(job)
    db_sess.commit()
    flash('Работа успешно удалена!', 'success')
    return redirect('/')

# Просмотр департаментов
@app.route('/departments')
@login_required
def departments():
    db_sess = db_session.create_session()
    deps = db_sess.query(Department).all()
    
    # Добавляем информацию о начальнике для каждого департамента
    for dep in deps:
        dep.chief_obj = db_sess.get(User, dep.chief)
    
    return render_template('department.html', departments=deps, current_user=current_user)

# Создание департамента
@app.route('/create_department', methods=['GET', 'POST'])
@login_required
def create_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dept = Department(
            title=form.title.data,
            chief=form.chief.data,
            members=form.members.data,
            email=form.email.data
        )
        db_sess.add(dept)
        db_sess.commit()
        
        flash('Департамент успешно добавлен!', 'success')
        return redirect('/departments')
    
    return render_template('create_department.html', form=form, title='Создание департамента')

# Редактирование департамента
@app.route('/edit_department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    db_sess = db_session.create_session()
    dept = db_sess.query(Department).get(id)
    
    if not dept:
        flash('Департамент не найден', 'danger')
        return redirect('/departments')
    
    # Проверка прав доступа: только начальник департамента или капитан (id=1)
    if current_user.id != dept.chief and current_user.id != 1:
        flash('У вас нет прав для редактирования этого департамента', 'danger')
        return redirect('/departments')
    
    form = DepartmentForm()
    
    if request.method == "GET":
        form.title.data = dept.title
        form.chief.data = dept.chief
        form.members.data = dept.members
        form.email.data = dept.email
    
    if form.validate_on_submit():
        dept.title = form.title.data
        dept.chief = form.chief.data
        dept.members = form.members.data
        dept.email = form.email.data
        
        db_sess.commit()
        flash('Департамент успешно обновлен!', 'success')
        return redirect('/departments')
    
    return render_template('create_department.html', form=form, title='Редактирование департамента')

# Удаление департамента
@app.route('/delete_department/<int:id>', methods=['POST'])
@login_required
def delete_department(id):
    db_sess = db_session.create_session()
    dept = db_sess.query(Department).get(id)
    
    if not dept:
        flash('Департамент не найден', 'danger')
        return redirect('/departments')
    
    # Проверка прав доступа: только начальник департамента или капитан (id=1)
    if current_user.id != dept.chief and current_user.id != 1:
        flash('У вас нет прав для удаления этого департамента', 'danger')
        return redirect('/departments')
    
    db_sess.delete(dept)
    db_sess.commit()
    flash('Департамент успешно удален!', 'success')
    return redirect('/departments')

# Управление категориями
@app.route('/categories')
@login_required
def categories():
    # Только капитан (id=1) может управлять категориями
    if current_user.id != 1:
        flash('Только капитан может просматривать категории', 'danger')
        return redirect('/')
    
    db_sess = db_session.create_session()
    cats = db_sess.query(Category).all()
    return render_template('categories.html', categories=cats, current_user=current_user)

@app.route('/create_category', methods=['GET', 'POST'])
@login_required
def create_category():
    # Только капитан (id=1) может создавать категории
    if current_user.id != 1:
        flash('Только капитан может создавать категории', 'danger')
        return redirect('/categories')
    
    form = CategoryForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Category).filter(Category.name == form.name.data).first():
            flash('Категория с таким названием уже существует', 'danger')
            return render_template('create_category.html', form=form)
        
        category = Category(
            name=form.name.data,
            description=form.description.data
        )
        db_sess.add(category)
        db_sess.commit()
        
        flash('Категория успешно добавлена!', 'success')
        return redirect('/categories')
    
    return render_template('create_category.html', form=form, title='Создание категории')

@app.route('/edit_category/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    # Только капитан (id=1) может редактировать категории
    if current_user.id != 1:
        flash('Только капитан может редактировать категории', 'danger')
        return redirect('/categories')
    
    db_sess = db_session.create_session()
    category = db_sess.query(Category).get(id)
    
    if not category:
        flash('Категория не найдена', 'danger')
        return redirect('/categories')
    
    form = CategoryForm()
    
    if request.method == "GET":
        form.name.data = category.name
        form.description.data = category.description
    
    if form.validate_on_submit():
        if category.name != form.name.data:
            if db_sess.query(Category).filter(Category.name == form.name.data).first():
                flash('Категория с таким названием уже существует', 'danger')
                return render_template('create_category.html', form=form)
        
        category.name = form.name.data
        category.description = form.description.data
        db_sess.commit()
        
        flash('Категория успешно обновлена!', 'success')
        return redirect('/categories')
    
    return render_template('create_category.html', form=form, title='Редактирование категории')

@app.route('/delete_category/<int:id>', methods=['POST'])
@login_required
def delete_category(id):
    # Только капитан (id=1) может удалять категории
    if current_user.id != 1:
        flash('Только капитан может удалять категории', 'danger')
        return redirect('/categories')
    
    db_sess = db_session.create_session()
    category = db_sess.query(Category).get(id)
    
    if not category:
        flash('Категория не найдена', 'danger')
        return redirect('/categories')
    
    # Проверяем, есть ли работы, связанные с этой категорией
    jobs_with_category = db_sess.query(Jobs).filter(Jobs.categories.contains(category)).all()
    if jobs_with_category:
        flash('Нельзя удалить категорию, так как с ней связаны работы. Сначала удалите связь с работами.', 'danger')
        return redirect('/categories')
    
    
    db_sess.delete(category)
    db_sess.commit()
    
    flash('Категория успешно удалена!', 'success')
    return redirect('/categories')

if __name__ == '__main__':
    # Создаем начальные данные только при первом запуске
    with app.app_context():
        create_initial_data()
    
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 Запуск сервера на http://127.0.0.1:{port}")
    print(f"🔧 Режим отладки: {'включен' if FLASK_DEBUG else 'выключен'}")
    app.run(host='127.0.0.1', port=port, debug=FLASK_DEBUG)
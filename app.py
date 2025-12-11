from flask import Flask, render_template, redirect
from data import db_session
from data.jobs import Jobs
from data.users import User
from data.departments import Department
from forms.user import RegisterForm
from forms.job import JobForm
from forms.department import DepartmentForm
import secrets, os

app = Flask(__name__)

FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"

if FLASK_DEBUG:
    # Для разработки: генерируем надёжный ключ
    secret_key = secrets.token_hex(32)
    app.config['SECRET_KEY'] = secret_key
    print(f"🔧 Сгенерирован секретный ключ: {secret_key}")
    print("⚠️  Этот ключ меняется при каждом запуске!")
else:
    # Для продакшена: получаем ключ из переменной окружения
    secret_key = os.environ.get('FLASK_SECRET_KEY')
    if not secret_key:
        raise RuntimeError("🚨 СЕКРЕТНЫЙ КЛЮЧ НЕ ЗАДАН! "
                           "Установите переменную окружения FLASK_SECRET_KEY для продакшена")
    app.config['SECRET_KEY'] = secret_key
    print("🛡️  [PRODUCTION MODE] Используется секретный ключ из переменной окружения")

DB_FILE = "mars_explorer.db"
db_session.global_init(DB_FILE)

@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("index.html", jobs=jobs)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
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
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/create_job', methods=['GET', 'POST'])
def create_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('create_job.html', title='Создание работы', form=form)

@app.route('/create_department', methods=['GET', 'POST'])
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
        return redirect('/')
    return render_template('create_department.html', title='Создание департамента', form=form)

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
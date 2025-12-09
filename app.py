# app.py
# Исправленный вариант: инициализация БД выполняется сразу, без декоратора before_first_request
# НАПИСАЛ СТУДЕНТ: ИМЯ_ФАМИЛИЯ, ГРУППА: ГРУППА

from flask import Flask, render_template, redirect, url_for
from data import db_session
from data.jobs import Jobs
from data.users import User
from data.departments import Department
from forms.user import RegisterForm
from forms.job import JobForm
from forms.department import DepartmentForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'

DB_FILE = "mars_explorer.db"


db_session.global_init(DB_FILE)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.is_finished != True).all()
    # подпись студента в шаблоне
    return render_template("index.html", jobs=jobs, student_name="ИМЯ_ФАМИЛИЯ", student_group="ГРУППА")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть",
                                   student_name="ИМЯ_ФАМИЛИЯ", student_group="ГРУППА")
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
        return redirect(url_for('index'))
    return render_template('register.html', title='Регистрация', form=form,
                           student_name="ИМЯ_ФАМИЛИЯ", student_group="ГРУППА")


@app.route('/create_job', methods=['GET', 'POST'])
def create_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        coll_raw = form.collaborators.data or ""
        coll_list = [int(x.strip()) for x in coll_raw.split(",") if x.strip().isdigit()]
        job = Jobs(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=coll_list,
            is_finished=form.is_finished.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect(url_for('index'))
    return render_template('create_job.html', title='Создать задачу', form=form,
                           student_name="ИМЯ_ФАМИЛИЯ", student_group="ГРУППА")


@app.route('/create_department', methods=['GET', 'POST'])
def create_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        members_raw = form.members.data or ""
        members = [int(x.strip()) for x in members_raw.split(",") if x.strip().isdigit()]
        dept = Department(
            title=form.title.data,
            chief=form.chief.data,
            members=members,
            email=form.email.data
        )
        db_sess.add(dept)
        db_sess.commit()
        return redirect(url_for('index'))
    return render_template('create_department.html', title='Создать департамент', form=form,
                           student_name="ИМЯ_ФАМИЛИЯ", student_group="ГРУППА")


if __name__ == "__main__":
    app.run(debug=True)

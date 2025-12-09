import sys
from datetime import datetime
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Department

def main(db_filename="mars_explorer.db"):
    db_session.global_init(db_filename)
    engine = db_session.get_engine()
    # создаём таблицы (SqlAlchemyBase — экспортируется в db_session)
    from data.db_session import SqlAlchemyBase
    SqlAlchemyBase.metadata.create_all(engine)

    session = db_session.create_session()

    # если нет капитана — добавим стартовые данные
    if not session.query(User).filter(User.email == "scott_chief@mars.org").first():
        captain = User(
            surname="Scott",
            name="Ridley",
            age=21,
            position="captain",
            speciality="research engineer",
            address="module_1",
            email="scott_chief@mars.org"
        )
        captain.set_password("secret")
        session.add(captain)
        session.flush()

        # добавим 5 колонистов (пример)
        c1 = User(surname="Watson", name="Emma", age=30, position="engineer", speciality="mechanic", address="module_1", email="emma.watson@mars.org")
        c1.set_password("1")
        c2 = User(surname="Kovacs", name="Ilya", age=17, position="technician", speciality="electronics", address="module_1", email="ilya.kovacs@mars.org")
        c2.set_password("1")
        c3 = User(surname="Lee", name="Anna", age=25, position="biologist", speciality="researcher", address="module_2", email="anna.lee@mars.org")
        c3.set_password("1")
        c4 = User(surname="Gonzalez", name="Carlos", age=40, position="chief_engineer", speciality="engineer", address="module_3", email="c.gonzalez@mars.org")
        c4.set_password("1")
        c5 = User(surname="Nguyen", name="Linh", age=22, position="middle_scientist", speciality="geologist", address="module_1", email="linh.nguyen@mars.org")
        c5.set_password("1")

        session.add_all([c1, c2, c3, c4, c5])
        session.flush()

        job = Jobs(
            team_leader=captain.id,
            job="deployment of residential modules 1 and 2",
            work_size=15,
            collaborators=[c1.id, c2.id],
            start_date=datetime.utcnow(),
            is_finished=False
        )
        session.add(job)

        dept = Department(
            title="Geological Exploration",
            chief=c5.id,
            members=[c3.id, c5.id],
            email="geo@mars.org"
        )
        session.add(dept)

        session.commit()
        print("DB created and filled with sample data.")
    else:
        print("DB already contains initial data.")

if __name__ == "__main__":
    db = sys.argv[1] if len(sys.argv) > 1 else input().strip()
    main(db)

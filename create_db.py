import sys
from datetime import datetime
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Department

def main(db_filename="mars_explorer.db"):
    db_session.global_init(db_filename)
    session = db_session.create_session()
    
    if not session.query(User).filter(User.email == "scott_chief@mars.org").first():
        # Создаем капитана
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
        
        # Создаем 5 колонистов
        colonists = [
            User(surname="Watson", name="Emma", age=30, position="engineer", speciality="mechanic", address="module_1", email="emma.watson@mars.org"),
            User(surname="Kovacs", name="Ilya", age=17, position="technician", speciality="electronics", address="module_1", email="ilya.kovacs@mars.org"),
            User(surname="Lee", name="Anna", age=25, position="biologist", speciality="researcher", address="module_2", email="anna.lee@mars.org"),
            User(surname="Gonzalez", name="Carlos", age=40, position="chief_engineer", speciality="engineer", address="module_3", email="c.gonzalez@mars.org"),
            User(surname="Nguyen", name="Linh", age=22, position="middle_scientist", speciality="geologist", address="module_1", email="linh.nguyen@mars.org")
        ]
        
        for c in colonists:
            c.set_password("password")
            session.add(c)
        
        session.flush()
        
        # Создаем первую работу
        job = Jobs(
            team_leader=captain.id,
            job="deployment of residential modules 1 and 2",
            work_size=15,
            collaborators="2, 3",
            start_date=datetime.now(),
            is_finished=False
        )
        session.add(job)
        
        # Создаем департамент
        dept = Department(
            title="Geological Exploration",
            chief=5,
            members="3, 5",
            email="geo@mars.org"
        )
        session.add(dept)
        
        session.commit()
        print("База данных успешно создана и заполнена начальными данными.")
    else:
        print("База данных уже содержит начальные данные.")

if __name__ == "__main__":
    db = sys.argv[1] if len(sys.argv) > 1 else "mars_explorer.db"
    main(db)
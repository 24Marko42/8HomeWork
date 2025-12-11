#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Система запросов для базы данных колонистов Марса
Использование:
    python mars_queries.py <номер_задачи> [<имя_бд>]
    
Доступные задачи:
    1  - Все колонисты в модуле 1
    2  - ID колонистов в модуле 1 без "engineer" в профессии/должности
    3  - Несовершеннолетние колонисты с указанием возраста
    4  - Колонисты с "chief" или "middle" в должности
    5  - Работы <20 часов, которые не завершены
    6  - Тимлиды работ с наибольшими командами
    7  - Изменить адрес для колонистов <21 года в module_1 на module_3
    8  - Сотрудники геологического департамента с >25 часов работы
"""

import sys
import os
from sqlalchemy import or_, func

# Настройка путей для импорта модулей
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

try:
    from data import db_session
    from data.users import User
    from data.jobs import Jobs
    from data.departments import Department
except ImportError as e:
    print(f"Ошибка импорта модулей: {e}")
    print("Убедитесь, что структура проекта соответствует ожидаемой:")
    print("data/")
    print("├── db_session.py")
    print("├── users.py")
    print("├── jobs.py")
    print("└── departments.py")
    sys.exit(1)

# === ЗАДАЧА 1: Все колонисты в модуле 1 ===
def query_module1_colonists(session):
    """Выводит всех колонистов, проживающих в первом модуле"""
    colonists = session.query(User).filter(User.address == "module_1").all()
    
    if not colonists:
        print("В модуле 1 нет колонистов")
        return
    
    print("Колонисты в модуле 1:")
    for i, colonist in enumerate(colonists, 1):
        print(f"{i}. {colonist}")

# === ЗАДАЧА 2: ID колонистов в модуле 1 без "engineer" в профессии/должности ===
def query_non_engineers_module1(session):
    """Выводит ID колонистов в module_1 без 'engineer' в speciality или position"""
    colonists = session.query(User).filter(
        User.address == "module_1",
        ~or_(
            User.speciality.ilike("%engineer%"),
            User.position.ilike("%engineer%")
        )
    ).all()
    
    if not colonists:
        print("Не найдено колонистов, соответствующих критериям")
        return
    
    print("ID колонистов в module_1 без 'engineer' в профессии/должности:")
    for colonist in colonists:
        print(colonist.id)

# === ЗАДАЧА 3: Несовершеннолетние колонисты с указанием возраста ===
def query_minors(session):
    """Выводит несовершеннолетних колонистов с указанием возраста"""
    minors = session.query(User).filter(User.age < 18).all()
    
    if not minors:
        print("Несовершеннолетних колонистов не найдено")
        return
    
    print("Несовершеннолетние колонисты:")
    for minor in minors:
        print(f"{minor} возраст: {minor.age} лет")

# === ЗАДАЧА 4: Колонисты с "chief" или "middle" в должности ===
def query_chief_middle(session):
    """Выводит колонистов с 'chief' или 'middle' в должности"""
    colonists = session.query(User).filter(
        or_(
            User.position.ilike("%chief%"),
            User.position.ilike("%middle%")
        )
    ).all()
    
    if not colonists:
        print("Колонистов с 'chief' или 'middle' в должности не найдено")
        return
    
    print("Колонисты с 'chief' или 'middle' в должности:")
    for colonist in colonists:
        print(colonist)

# === ЗАДАЧА 5: Работы <20 часов, которые не завершены ===
def query_short_jobs(session):
    """Выводит работы, требующие меньше 20 часов и не завершенные"""
    jobs = session.query(Jobs).filter(
        Jobs.work_size < 20,
        Jobs.is_finished == False
    ).all()
    
    if not jobs:
        print("Работ, требующих меньше 20 часов и не завершенных, не найдено")
        return
    
    print("Работы (<20 часов, не завершены):")
    for job in jobs:
        print(job)

# === ЗАДАЧА 6: Тимлиды работ с наибольшими командами ===
def query_largest_teams(session):
    """Выводит тимлидов работ с наибольшими командами"""
    all_jobs = session.query(Jobs).all()
    
    if not all_jobs:
        print("Работ не найдено")
        return
    
    # Вычисляем размер команды для каждой работы
    jobs_with_team_size = []
    for job in all_jobs:
        team_size = 0
        if job.collaborators:
            # Учитываем формат хранения: "2,3" или "[2,3]" или "2 3"
            collaborators_str = job.collaborators.strip('[] ')
            if collaborators_str:
                team_size = len([c.strip() for c in collaborators_str.split(',') if c.strip()])
        jobs_with_team_size.append((job, team_size))
    
    # Находим максимальный размер команды
    max_team_size = max(size for _, size in jobs_with_team_size)
    
    # Находим все работы с максимальным размером команды
    largest_jobs = [job for job, size in jobs_with_team_size if size == max_team_size]
    
    print(f"Работы с максимальным размером команды ({max_team_size} участников):")
    for i, job in enumerate(largest_jobs, 1):
        leader = session.query(User).filter(User.id == job.team_leader).first()
        leader_name = f"{leader.surname} {leader.name}" if leader else f"ID {job.team_leader} (не найден)"
        collaborators = job.collaborators or "не указаны"
        print(f"{i}. Работа: {job.job}")
        print(f"   Тимлид: {leader_name}")
        print(f"   Команда: {collaborators} (размер: {max_team_size})")

# === ЗАДАЧА 7: Изменить адрес для колонистов <21 года в module_1 ===
def query_update_addresses(session):
    """Изменяет адрес колонистов <21 года в module_1 на module_3"""
    young_colonists = session.query(User).filter(
        User.address == "module_1",
        User.age < 21
    ).all()
    
    if not young_colonists:
        print("Не найдено колонистов в module_1 младше 21 года для изменения адреса")
        return
    
    print(f"Найдено {len(young_colonists)} колонистов для изменения адреса:")
    for colonist in young_colonists:
        print(f"  - {colonist}, возраст: {colonist.age}, текущий адрес: {colonist.address}")
    
    confirmation = input("\nПодтвердите изменение адресов на 'module_3' (y/n): ").strip().lower()
    if confirmation != 'y':
        print("Изменение отменено")
        return
    
    # Изменяем адреса
    for colonist in young_colonists:
        old_address = colonist.address
        colonist.address = "module_3"
        print(f"Адрес изменен для {colonist}: {old_address} -> module_3")
    
    session.commit()
    print(f"\n✅ Успешно изменен адрес для {len(young_colonists)} колонистов")

# === ЗАДАЧА 8: Сотрудники геологического департамента с >25 часов работы ===
def query_department_hours(session):
    """Выводит сотрудников геологического департамента с >25 часов работы"""
    # Ищем геологический департамент
    geo_dept = session.query(Department).filter(
        or_(
            Department.title.ilike("%geological%"),
            Department.title.ilike("%геолог%")
        )
    ).first()
    
    if not geo_dept:
        print("Геологический департамент не найден")
        return
    
    print(f"Найден департамент: {geo_dept.title} (ID: {geo_dept.id})")
    
    # Получаем ID участников департамента
    member_ids = []
    if geo_dept.members:
        # Очищаем строку от лишних символов и разделяем
        members_str = geo_dept.members.strip('[] ')
        if members_str:
            member_ids = [int(id_str.strip()) for id_str in members_str.split(',') if id_str.strip().isdigit()]
    
    if not member_ids:
        print("В департаменте нет участников")
        return
    
    print(f"Участники департамента (ID): {', '.join(map(str, member_ids))}")
    
    # Находим сотрудников с >25 часов работы
    qualified_members = []
    for member_id in member_ids:
        # Считаем суммарное время выполненных работ
        total_hours = session.query(func.sum(Jobs.work_size)).filter(
            Jobs.team_leader == member_id,
            Jobs.is_finished == True
        ).scalar() or 0
        
        if total_hours > 25:
            member = session.query(User).filter(User.id == member_id).first()
            if member:
                qualified_members.append((member, total_hours))
    
    if not qualified_members:
        print("Сотрудников с суммарным временем работы >25 часов не найдено")
        return
    
    print("\nСотрудники геологического департамента с суммарным временем работы >25 часов:")
    for member, hours in qualified_members:
        print(f"{member.surname} {member.name} (ID: {member.id}) - {hours} часов")

# === ОСНОВНАЯ ФУНКЦИЯ ===
def main():
    # Словарь задач
    tasks = {
        '1': ('Все колонисты в модуле 1', query_module1_colonists),
        '2': ('ID колонистов в module_1 без "engineer" в профессии/должности', query_non_engineers_module1),
        '3': ('Несовершеннолетние колонисты', query_minors),
        '4': ('Колонисты с "chief" или "middle" в должности', query_chief_middle),
        '5': ('Работы <20 часов, не завершенные', query_short_jobs),
        '6': ('Тимлиды работ с наибольшими командами', query_largest_teams),
        '7': ('Изменить адрес для колонистов <21 года в module_1', query_update_addresses),
        '8': ('Сотрудники геол. департамента с >25 часов работы', query_department_hours),
    }
    
    # Парсинг аргументов
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nДоступные задачи:")
        for key, (desc, _) in tasks.items():
            print(f"  {key} - {desc}")
        sys.exit(0)
    
    task_number = sys.argv[1]
    db_file = sys.argv[2] if len(sys.argv) > 2 else input("Введите имя базы данных: ").strip()
    
    if task_number not in tasks:
        print(f"Ошибка: задача '{task_number}' не существует")
        print("Доступные задачи:", ", ".join(tasks.keys()))
        sys.exit(1)
    
    task_name, task_function = tasks[task_number]
    print(f"\n{'='*60}")
    print(f"ЗАДАЧА {task_number}: {task_name}")
    print(f"База данных: {db_file}")
    print(f"{'='*60}\n")
    
    try:
        # Инициализация сессии
        db_session.global_init(db_file)
        session = db_session.create_session()
        
        # Выполнение задачи
        task_function(session)
        
        # Закрытие сессии
        session.close()
        print(f"\n{'='*60}")
        print(f"Задача {task_number} выполнена успешно")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"\n{'!'*60}")
        print(f"ОШИБКА при выполнении задачи {task_number}:")
        print(f"{str(e)}")
        print(f"{'!'*60}")
        sys.exit(1)

if __name__ == "__main__":
    main()
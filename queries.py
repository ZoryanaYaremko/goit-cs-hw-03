import psycopg2

try:
    # Підключення до бази даних PostgreSQL
    conn = psycopg2.connect(
        dbname="task_management_db",  
        user="postgres",              
        password="NatalyaBoyko3105$",     
        host="localhost",             
        port="5432",
        client_encoding='UTF8'
    )
    
    # Створення курсору для виконання SQL запитів
    cur = conn.cursor()
    
    print("З'єднання встановлено успішно")
    
    # Виконання SQL запиту для перевірки версії
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    print(f"Версія PostgreSQL: {db_version}")

    # 1. Отримати всі завдання певного користувача
    user_id = 1  # Приклад user_id
    cur.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
    tasks_for_user = cur.fetchall()
    print("Завдання користувача:", tasks_for_user)

    # 2. Вибрати завдання за певним статусом
    status_name = 'new'  # Приклад статусу
    cur.execute("""
        SELECT * FROM tasks WHERE status_id = (
            SELECT id FROM status WHERE name = %s
        )
    """, (status_name,))
    tasks_with_status = cur.fetchall()
    print("Завдання зі статусом:", tasks_with_status)

    # 3. Оновити статус конкретного завдання
    task_id = 1  # Приклад task_id
    new_status_id = 2  # Приклад нового статусу
    cur.execute("UPDATE tasks SET status_id = %s WHERE id = %s", (new_status_id, task_id))
    conn.commit()

    # 4. Отримати список користувачів, які не мають жодного завдання
    cur.execute("""
        SELECT * FROM users WHERE id NOT IN (
            SELECT user_id FROM tasks
        )
    """)
    users_without_tasks = cur.fetchall()
    print("Користувачі без завдань:", users_without_tasks)

    # 5. Додати нове завдання для конкретного користувача
    new_task_title = "Нове завдання"
    new_task_description = "Опис нового завдання"
    new_task_user_id = 1  # Приклад user_id
    new_task_status_id = 1  # Приклад статусу
    cur.execute("INSERT INTO tasks (title, description, user_id, status_id) VALUES (%s, %s, %s, %s)", 
                (new_task_title, new_task_description, new_task_user_id, new_task_status_id))
    conn.commit()

    # 6. Отримати всі завдання, які ще не завершено
    cur.execute("""
        SELECT * FROM tasks WHERE status_id != (
            SELECT id FROM status WHERE name = 'completed'
        )
    """)
    incomplete_tasks = cur.fetchall()
    print("Незавершені завдання:", incomplete_tasks)

    # 7. Видалити конкретне завдання
    task_id_to_delete = 1  # Приклад task_id
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id_to_delete,))
    conn.commit()

    # 8. Знайти користувачів з певною електронною поштою
    email_domain = "%@gmail.com"  # Приклад фільтра за доменом
    cur.execute("SELECT * FROM users WHERE email LIKE %s", (email_domain,))
    users_with_domain = cur.fetchall()
    print("Користувачі з доменом:", users_with_domain)

    # 9. Оновити ім'я користувача
    new_fullname = "Новий Ім'я"
    user_id_to_update = 1  # Приклад user_id
    cur.execute("UPDATE users SET fullname = %s WHERE id = %s", (new_fullname, user_id_to_update))
    conn.commit()

    # 10. Отримати кількість завдань для кожного статусу
    cur.execute("""
        SELECT s.name, COUNT(t.id) 
        FROM tasks t 
        JOIN status s ON t.status_id = s.id 
        GROUP BY s.name
    """)
    task_count_by_status = cur.fetchall()
    print("Кількість завдань за статусами:", task_count_by_status)

except Exception as e:
    print(f"Виникла помилка при підключенні до бази даних: {e}")

finally:
    # Закриття курсора та з'єднання
    if cur:
        cur.close()
    if conn:
        conn.close()
    print("З'єднання закрито")




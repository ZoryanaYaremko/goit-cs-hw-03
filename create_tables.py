import psycopg2

# Підключення до бази даних
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

# Створення таблиці users
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100),
        email VARCHAR(100) UNIQUE
    );
''')

# Створення таблиці status
cur.execute('''
    CREATE TABLE IF NOT EXISTS status (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE
    );
''')

# Створення таблиці tasks
cur.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100),
        description TEXT,
        status_id INTEGER REFERENCES status(id),
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
    );
''')

# Збереження змін і закриття з'єднання
conn.commit()
cur.close()
conn.close()

print("Таблиці успішно створено.")

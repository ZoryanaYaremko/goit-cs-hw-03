import psycopg2
from faker import Faker

# Підключення до бази даних
conn = psycopg2.connect(
        dbname="task_management_db",  
        user="postgres",              
        password="NatalyaBoyko3105$",     
        host="localhost",             
        port="5432",
        client_encoding='UTF8'
)

# Створення курсору
cur = conn.cursor()

# Ініціалізація Faker
faker = Faker()

# Заповнення таблиці status
statuses = ['new', 'in progress', 'completed']
for status in statuses:
    cur.execute("INSERT INTO status (name) VALUES (%s) ON CONFLICT DO NOTHING", (status,))

# Заповнення таблиці users
for _ in range(10):
    fullname = faker.name()
    email = faker.email()
    cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s) ON CONFLICT DO NOTHING", (fullname, email))

# Заповнення таблиці tasks
cur.execute("SELECT id FROM users")
user_ids = cur.fetchall()

cur.execute("SELECT id FROM status")
status_ids = cur.fetchall()

for _ in range(20):
    title = faker.sentence(nb_words=4)
    description = faker.text()
    user_id = faker.random.choice(user_ids)[0]
    status_id = faker.random.choice(status_ids)[0]
    cur.execute("INSERT INTO tasks (title, description, user_id, status_id) VALUES (%s, %s, %s, %s)", 
                (title, description, user_id, status_id))

# Збереження змін і закриття з'єднання
conn.commit()
cur.close()
conn.close()

print("Таблиці успішно заповнено випадковими даними.")

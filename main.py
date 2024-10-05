from pymongo import MongoClient
from bson.objectid import ObjectId

# Підключення до локальної MongoDB або MongoDB Atlas
client = MongoClient("mongodb://localhost:27017/")  # Для MongoDB Atlas замініть URI

# Вибір бази даних
db = client["cats_database"]
# Вибір колекції
cats_collection = db["cats"]

# CRUD функції

# Create (Додавання нового документа в колекцію)
def create_cat(name, age, features):
    new_cat = {
        "name": name,
        "age": age,
        "features": features
    }
    result = cats_collection.insert_one(new_cat)
    print(f"Новий кіт доданий з ID: {result.inserted_id}")

# Read (Виведення всіх записів)
def get_all_cats():
    cats = cats_collection.find()
    for cat in cats:
        print(cat)

# Read (Пошук кота за ім'ям)
def get_cat_by_name(name):
    cat = cats_collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print(f"Кіт з ім'ям {name} не знайдений")

# Update (Оновлення віку кота за ім'ям)
def update_cat_age(name, new_age):
    result = cats_collection.update_one(
        {"name": name},
        {"$set": {"age": new_age}}
    )
    if result.matched_count > 0:
        print(f"Вік кота {name} оновлено до {new_age}")
    else:
        print(f"Кіт з ім'ям {name} не знайдений")

# Update (Додавання нової характеристики до кота за ім'ям)
def add_feature_to_cat(name, new_feature):
    result = cats_collection.update_one(
        {"name": name},
        {"$push": {"features": new_feature}}
    )
    if result.matched_count > 0:
        print(f"До кота {name} додано характеристику: {new_feature}")
    else:
        print(f"Кіт з ім'ям {name} не знайдений")

# Delete (Видалення кота за ім'ям)
def delete_cat_by_name(name):
    result = cats_collection.delete_one({"name": name})
    if result.deleted_count > 0:
        print(f"Кіт з ім'ям {name} видалений")
    else:
        print(f"Кіт з ім'ям {name} не знайдений")

# Delete (Видалення всіх записів)
def delete_all_cats():
    result = cats_collection.delete_many({})
    print(f"Видалено {result.deleted_count} котів")

# Приклад виконання функцій
if __name__ == "__main__":
    # Додавання нового кота
    create_cat("barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])

    # Виведення всіх котів
    print("Всі коти в базі:")
    get_all_cats()

    # Пошук кота за ім'ям
    print("Інформація про кота 'barsik':")
    get_cat_by_name("barsik")

    # Оновлення віку кота
    update_cat_age("barsik", 5)

    # Додавання нової характеристики коту
    add_feature_to_cat("barsik", "любить рибу")

    # Видалення кота за ім'ям
    delete_cat_by_name("barsik")

    # Видалення всіх котів
    delete_all_cats()

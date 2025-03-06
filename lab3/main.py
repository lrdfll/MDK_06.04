import json

def load_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден.")
        return None
    except json.JSONDecodeError:
        print("Ошибка: неверный формат JSON.")
        return None

def recommend_books(user_preferences, books):
    recommended_books = []
    for book in books:
        if (book["author"] == user_preferences["author"] and
            book["genre"] == user_preferences["genre"] and
            book["age_group"] == user_preferences["age_group"]):
            recommended_books.append(book["title"])
    return recommended_books

if __name__ == "__main__":
    file_path = "books.json"
    data = load_data(file_path)
    if not data:
        exit(1)

    books = data.get("books", [])

    print("Введите ваши предпочтения:")
    user_input = {
        "author": input("Автор: ").strip(),
        "genre": input("Жанр: ").strip(),
        "age_group": input("Возрастная группа (6+, 12+, 16+, 18+): ").strip()
    }

    recommendations = recommend_books(user_input, books)

    if recommendations:
        print("\nРекомендуемые книги:", recommendations)
    else:
        print("\nПодходящих книг не найдено.")
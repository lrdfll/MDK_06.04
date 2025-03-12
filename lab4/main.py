from docx import Document
import os
from datetime import datetime

# Правила для напоминаний
rules = [
    {
        "condition": lambda data: data["current_time"] == data["medication_time"] and data["method"] == "до еды",
        "action": "Примите лекарство до еды"
    },
    {
        "condition": lambda data: data["current_time"] == data["medication_time"] and data["method"] == "после еды",
        "action": "Примите лекарство после еды"
    },
    {
        "condition": lambda data: data["current_time"] == data["medication_time"] and data["method"] == "независимо от еды",
        "action": "Примите лекарство независимо от еды"
    },
    {
        "condition": lambda data: data["current_time"] > data["medication_time"] and data["status"] == "не принято",
        "action": lambda data: f"Вы пропустили прием лекарства в {data['medication_time']}. Примите его как можно скорее"
    },
    {
        "condition": lambda data: data["current_time"] != data["medication_time"],
        "action": lambda data: f"Следующий прием лекарства в {data['medication_time']}"
    }
]

# Функция для чтения данных из файла
def read_questionnaire(file_path):
    try:
        doc = Document(file_path)
        data = {}
        for paragraph in doc.paragraphs:
            if ": " in paragraph.text:
                # Удаляем лишние символы (например, "1.", "2.", и т.д.)
                text = paragraph.text.strip()
                if text.startswith(("1.", "2.", "3.", "4.")):
                    text = text[2:].strip()  # Удаляем первые два символа
                parts = text.split(": ", 1)
                key = parts[0].strip()
                value = parts[1].strip().lower() if len(parts) > 1 else ""
                data[key] = value

        # Преобразование данных
        data["medication_time"] = data.get("Время приема лекарства (в формате ЧЧ:ММ)", "").strip()
        data["method"] = data.get("Способ применения (до еды/после еды/независимо от еды)", "").strip().lower()
        data["current_time"] = data.get("Текущее время (в формате ЧЧ:ММ)", "").strip()
        data["status"] = data.get("Статус приема лекарства (принято/не принято)", "").strip().lower()

        # Преобразуем время в объекты datetime.time для корректного сравнения
        try:
            data["medication_time"] = datetime.strptime(data["medication_time"], "%H:%M").time()
            data["current_time"] = datetime.strptime(data["current_time"], "%H:%M").time()
        except ValueError:
            print("Ошибка: неверный формат времени. Используйте формат ЧЧ:ММ.")
            return None

        return data
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

# Функция для анализа данных и вывода напоминаний
def analyze_data(data):
    required_fields = ["medication_time", "method", "current_time", "status"]
    if not all(data.get(field) is not None for field in required_fields):
        print("Ошибка: не все данные заполнены.")
        return

    matched = False
    for rule in rules:
        if rule["condition"](data):
            action = rule["action"](data) if callable(rule["action"]) else rule["action"]
            print(action)
            matched = True

    if not matched:
        print("Нет напоминаний на текущий момент.")

# Основная часть программы
if __name__ == "__main__":
    # Укажите путь к файлу
    file_path = "Анкета.docx"

    # Проверка наличия файла
    if not os.path.exists(file_path):
        print(f"Файл '{file_path}' не найден. Убедитесь, что файл существует и путь указан правильно.")
    else:
        # Чтение данных из файла
        data = read_questionnaire(file_path)
        if data:
            # Анализ данных и вывод напоминаний
            analyze_data(data)
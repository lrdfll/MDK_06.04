import xml.etree.ElementTree as ET
import json
import random
import matplotlib.pyplot as plt
import pandas as pd

def generate_sales_data(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    data = {}

    for offer in root.findall(".//offer"):
        name = offer.find('name').text
        data[name] = [random.randint(10, 30) for _ in range(12)]

    return data

def visualize_sales_data(data):
    months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
              "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

    plt.figure(figsize=(10, 6))
    for name, sales in data.items():
        plt.plot(months, sales, marker='o', label=name)

    plt.xlabel("Месяц")
    plt.ylabel("Количество продаж")
    plt.title("Динамика продаж мебели по месяцам")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.show()

def create_sales_table(data):
    months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
              "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
    df = pd.DataFrame(data, index=months)
    print(df)

def save_json_file(data, json_file):
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

xml_file = 'catalog.xml'
json_file = 'data.json'
data = generate_sales_data(xml_file)
save_json_file(data, json_file)
visualize_sales_data(data)
create_sales_table(data)
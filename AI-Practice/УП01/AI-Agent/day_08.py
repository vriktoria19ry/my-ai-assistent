import pandas as pd
import matplotlib.pyplot as plt
import os

print("=" * 50)
print("Запуск day_08.py...")
 
if not os.path.exists("students.csv"):
    print("Файл students.csv не найден. Создаём его с базовыми данными.")
    base_data = {
        'Имя': ['Иван', 'Анна', 'Пётр', 'Мария'],
        'Группа': ['1ИИ-1', '1ИИ-1', '1ИИ-2', '1ИИ-2'],
        'Баллы': [85, 92, 76, 88],
        'Посещено': [18, 20, 15, 19]
    }
    pd.DataFrame(base_data).to_csv("students.csv", index=False, encoding="utf-8")
 
try:
    df = pd.read_csv("students.csv")
    print("Данные успешно загружены в переменную 'df'.")
    print(df.head())
except Exception as e:
    print(f"Критическая ошибка при чтении файла: {e}")
    exit()  

print("=" * 50)

  
print("\n--- Выполнение Задания 25 ---")
 
group_stats = df.groupby("Группа").agg({
    "Баллы": ["mean", "min", "max", "count"],
    "Посещено": "mean"
})
 
group_stats.columns = ["_".join(col).strip() for col in group_stats.columns.values]
group_stats = group_stats.reset_index()
group_stats.rename(columns={
    "Баллы_mean": "Средний_балл",
    "Баллы_min": "Минимум",
    "Баллы_max": "Максимум",
    "Баллы_count": "Количество_студентов",
    "Посещено_mean": "Средняя_посещаемость"
}, inplace=True)

print("Итоговая таблица по группам:")
print(group_stats)
 
group_stats.to_csv("group_summary_day25.csv", index=False, encoding="utf-8")
print("Таблица сохранена в group_summary_day25.csv")
 
plt.figure(figsize=(8, 5))
plt.bar(group_stats["Группа"], group_stats["Средний_балл"], color='mediumpurple')
plt.title("Средний балл по учебным группам")
plt.xlabel("Группа")
plt.ylabel("Средний балл")
plt.ylim(0, 100)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("group_avg_score_plot.png")
plt.close()
print("График среднего балла сохранен в group_avg_score_plot.png")

 
print("\n--- Выполнение Задания 26 ---")
 
if os.path.exists("products.csv"):
    df_products = pd.read_csv("products.csv")
    print("Файл products.csv загружен.")
else:
    print("Файл products.csv не найден. Создаём его.")
    prod_data = {
        'Категория': ['Электроника', 'Электроника', 'Бытовая техника', 'Бытовая техника', 'Электроника', 'Книги', 'Книги'],
        'Товар': ['Смартфон', 'Ноутбук', 'Чайник', 'Микроволновка', 'Наушники', 'Учебник', 'Роман'],
        'Цена': [50000, 85000, 3000, 7000, 5000, 1500, 800],
        'Количество': [15, 8, 50, 20, 100, 200, 300]
    }
    df_products = pd.DataFrame(prod_data)
    df_products.to_csv("products.csv", index=False, encoding="utf-8")

category_stats = df_products.groupby("Категория").agg({
    "Цена": "mean",
    "Количество": "sum"
}).reset_index()
category_stats.rename(columns={"Цена": "Средняя_цена", "Количество": "Общее_количество"}, inplace=True)

print("Итоговая таблица по категориям товаров:")
print(category_stats)

category_stats.to_csv("category_summary_day26.csv", index=False, encoding="utf-8")
print("Таблица сохранена в category_summary_day26.csv")
 
plt.figure(figsize=(8, 5))
plt.bar(category_stats["Категория"], category_stats["Средняя_цена"], color='coral')
plt.title("Средняя цена по категориям товаров")
plt.xlabel("Категория")
plt.ylabel("Средняя цена")
plt.tight_layout()
plt.savefig("category_avg_price_plot.png")
plt.close()
print("График средней цены сохранен в category_avg_price_plot.png")

print("\n=== ВЫПОЛНЕНИЕ ЗАВЕРШЕНО УСПЕШНО ===")
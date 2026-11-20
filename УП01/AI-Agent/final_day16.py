from pathlib import Path
import csv

def clean_text(text: str) -> str:
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())

categories_map = {
    "algo_sorting.txt": "Sorting",
    "algo_search.txt": "Search",
    "data_structures.txt": "Data Structures",
    "complexity.txt": "Complexity",
    "recursion.txt": "Recursion",
    "greedy_methods.txt": "Greedy Algorithms"
}

corpus_dir = Path("corpus")
cleaned_dir = Path("cleaned")
csv_file = Path("corpus_summary.csv")
short_threshold = 50

if not corpus_dir.exists():
    print(f"Ошибка: Папка '{corpus_dir}' не найдена!")
    exit(1)

cleaned_dir.mkdir(exist_ok=True)
files = list(corpus_dir.glob("*.txt"))
print(f"Найдено файлов: {len(files)}\n")

documents = []

for file_path in files:
    try:
        raw = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Не удалось прочитать {file_path.name}: {e}")
        continue

    if not raw:
        print(f"[!] Пропущен пустой файл: {file_path.name}")
        continue

    cleaned = clean_text(raw)
    length = len(cleaned)

    if length < short_threshold:
        print(f"   [⚠️] Слишком короткий документ: {file_path.name} ({length} символов)")

    category = categories_map.get(file_path.name, "other")
    
    doc = {
        "source": file_path.name,
        "category": category,
        "text": cleaned,
        "length": length
    }
    documents.append(doc)

    (cleaned_dir / file_path.name).write_text(cleaned, encoding="utf-8")

avg_length = sum(d["length"] for d in documents) / len(documents) if documents else 0

print("\n--- Таблица корпуса ---")
print(f"{'Файл':<30} | {'Категория':<20} | {'Символов'}")
print("-" * 68)
for d in documents:
    print(f"{d['source']:<30} | {d['category']:<20} | {d['length']}")

total = sum(d["length"] for d in documents)
longest = max(documents, key=lambda d: d["length"])
shortest = min(documents, key=lambda d: d["length"])

print("\n=== ИТОГИ ===")
print(f"Количество документов в корпусе: {len(documents)}")
print(f"Суммарный объём корпуса: {total} символов")
print(f"Средняя длина документа: {avg_length:.1f} символов")  
print(f"Самый длинный документ: {longest['source']} ({longest['length']} символов)")
print(f"Самый короткий документ: {shortest['source']} ({shortest['length']} символов)")

with csv_file.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["source", "category", "length"])
    writer.writeheader()
    for d in documents:
        writer.writerow({
            "source": d["source"],
            "category": d["category"],
            "length": d["length"]
        })

print(f"\n✅ Сводка сохранена в файл: {csv_file.resolve()}")

import os
from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import ChatCompletionRequest, ChatMessage, ChatModelOptions

# 1. Загрузка переменных окружения
load_dotenv()
credentials = os.getenv("GIGACHAT_CREDENTIALS")
scope = os.getenv("GIGACHAT_SCOPE")

if not credentials or not scope:
    print("Ошибка: не найдены переменные GIGACHAT_CREDENTIALS или GIGACHAT_SCOPE в .env")
    exit(1)

# 2. Системный промпт (общие правила помощника)
system_prompt = (
    "Ты помощник по организации мероприятий. "
    "Отвечай строго в трёх разделах: Концепция, Смета, План действий. "
    "Если в запросе нет данных для какого-либо поля — пиши «не указано». "
    "Не выдумывай данные, которых нет в запросе. "
    "Избегай повторов, формулируй пункты разнообразно."
)

# 3. Сбор входных данных (добавлено обязательное поле «Целевая аудитория»)
goal = input("Цель мероприятия (обязательно): ").strip()
target_audience = input("Целевая аудитория (обязательно, например «дети 5–7 лет», «подростки 13–17»): ").strip()
limit = input("Ограничения (бюджет, площадка, сроки и т.п.): ").strip()
desired_outcome = input("Желаемый итог: ").strip()

while True:
    format_choice = input("Формат ответа (введите «краткий» или «пошаговый»): ").strip().lower()
    if format_choice in ["краткий", "пошаговый"]:
        break
    else:
        print("Неверный выбор. Введите «краткий» или «пошаговый».")

# 4. Валидация (теперь два обязательных поля: цель и аудитория)
if not goal:
    print("Ошибка: цель мероприятия обязательна. Запрос не отправлен.")
    exit(0)

if not target_audience:
    print("Ошибка: целевая аудитория обязательна. Запрос не отправлен.")
    exit(0)

# 5. Формирование user_prompt через f-строку (включено новое поле и акцент на учёте аудитории)
user_prompt = (
    f"Придумай мероприятие по следующим данным:\n"
    f"- Цель: {goal}\n"
    f"- Целевая аудитория: {target_audience}\n"
    f"- Ограничения: {limit if limit else 'не указано'}\n"
    f"- Желаемый итог: {desired_outcome if desired_outcome else 'не указано'}\n\n"
    f"Формат ответа: {format_choice}.\n"
    f"Если каких-то данных нет — пиши «не указано». Не придумывай данные.\n"
    f"Ответ дай строго в трёх разделах: Концепция, Смета, План действий.\n"
    f"Учитывай возраст и интересы целевой аудитории при подборе активностей и формулировках."
)

print("\n--- Сформированный запрос (user_prompt) ---")
print(user_prompt)
print("------------------------------------------\n")

# 6. Параметры и вызов GigaChat (сохранены оптимальные настройки из экспериментов)
options = ChatModelOptions(
    temperature=0.3,
    max_tokens=500,
    repetition_penalty=1.05,
    top_p=0.8
)

messages = [
    ChatMessage(role="system", content=system_prompt),
    ChatMessage(role="user", content=user_prompt),
]

request = ChatCompletionRequest(model="GigaChat-2", messages=messages, model_options=options)

try:
    with GigaChat(credentials=credentials, scope=scope, ca_bundle_file="certs/russian_trusted_root_ca_pem.crt") as client:
        response = client.chat.create(request)
        answer_text = response.messages[0].content[0].text
except Exception as e:
    print(f"Ошибка при запросе к GigaChat: {e}")
    exit(0)

# Вывод ответа
print("\n--- Ответ модели ---")
print(answer_text)
print("--------------------\n")

# 7. Сохранение файлов (только при успехе, UTF-8, без ключа API)
with open("last_prompt.txt", "w", encoding="utf-8") as f:
    f.write(user_prompt)

with open("last_answer.txt", "w", encoding="utf-8") as f:
    f.write(answer_text)

print("Файлы last_prompt.txt и last_answer.txt успешно обновлены.")

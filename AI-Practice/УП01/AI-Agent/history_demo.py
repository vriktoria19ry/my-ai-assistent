
max_pairs = 3

messages = [
    {"role": "system", "content": "Ты помощник по мероприятиям"},
    {"role": "user", "content": "Хочу день рождения на 10 человек"},
    {"role": "assistant", "content": "Вариант 1: лофт + ведущий"},
    {"role": "user", "content": "А бюджет 20к?"},
    {"role": "assistant", "content": "Тогда без ведущего, зато торт крутой"},
    {"role": "user", "content": "Ещё варианты?"},
    {"role": "assistant", "content": "Вариант 2: пикник в парке"},
    {"role": "user", "content": "Третий вариант?"},
    {"role": "assistant", "content": "Вариант 3: домашняя вечеринка с настолками"},
    {"role": "user", "content": "Для третьего распиши план"},
    {"role": "assistant", "content": "План: купить игры, заказать пиццу, подготовить плейлист"},
]

print("До обрезки:")
for i, m in enumerate(messages):
    print(f"{i}: [{m['role']}] {m['content'][:40]}")
print(f"Длина до: {len(messages)}\n")

k = 2 * max_pairs
if len(messages) > 1 + k:
    messages = [messages[0]] + messages[-k:]

print("После обрезки:")
for i, m in enumerate(messages):
    print(f"{i}: [{m['role']}] {m['content'][:40]}")
print(f"Длина после: {len(messages)}")
print(f"Ожидаемая длина: 1 (system) + {k} = {1 + k}")

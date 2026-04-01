"""
Пожалуйста, приступайте к этой задаче после того, как вы сделали и получили ревью ко всем остальным задачам
в этом репозитории. Она значительно сложнее.


Есть набор сообщений из чата в следующем формате:

```
messages = [
    {
        "id": "efadb781-9b04-4aad-9afe-e79faef8cffb",
        "sent_at": datetime.datetime(2022, 10, 11, 23, 11, 11, 721),
        "sent_by": 46,  # id пользователя-отправителя
        "reply_for": "7b22ae19-6c58-443e-b138-e22784878581",  # id сообщение, на которое это сообщение является ответом (может быть None)
        "seen_by": [26, 91, 71], # идентификаторы пользователей, которые видели это сообщение
        "text": "А когда ревью будет?",
    }
]
```

Так же есть функция `generate_chat_history`, которая вернёт список из большого количества таких сообщений.
Установите библиотеку lorem, чтобы она работала.

Нужно:
1. Вывести айди пользователя, который написал больше всех сообщений.
2. Вывести айди пользователя, на сообщения которого больше всего отвечали.
3. Вывести айди пользователей, сообщения которых видело больше всего уникальных пользователей.
4. Определить, когда в чате больше всего сообщений: утром (до 12 часов), днём (12-18 часов) или вечером (после 18 часов).
5. Вывести идентификаторы сообщений, который стали началом для самых длинных тредов (цепочек ответов).

Весь код стоит разбить на логические части с помощью функций.

import random
import uuid
import datetime

import lorem


def generate_chat_history():
    messages_amount = random.randint(200, 1000)
    users_ids = list(
        {random.randint(1, 10000) for _ in range(random.randint(5, 20))}
    )
    sent_at = datetime.datetime.now() - datetime.timedelta(days=100)
    messages = []
    for _ in range(messages_amount):
        sent_at += datetime.timedelta(minutes=random.randint(0, 240))
        messages.append({
            "id": uuid.uuid4(),
            "sent_at": sent_at,
            "sent_by": random.choice(users_ids),
            "reply_for": random.choice(
                [
                    None,
                    (
                        random.choice([m["id"] for m in messages])
                        if messages else None
                    ),
                ],
            ),
            "seen_by": random.sample(users_ids, random.randint(1, len(users_ids))),
            "text": lorem.sentence(),
        })
    return messages


if __name__ == "__main__":
    print(generate_chat_history())
"""


import random
import uuid
import datetime
from collections import defaultdict, Counter

import lorem


def generate_chat_history():
    """Генерирует историю чата"""
    messages_amount = random.randint(200, 1000)
    users_ids = list(
        {random.randint(1, 10000) for _ in range(random.randint(5, 20))}
    )
    sent_at = datetime.datetime.now() - datetime.timedelta(days=100)
    messages = []
    for _ in range(messages_amount):
        sent_at += datetime.timedelta(minutes=random.randint(0, 240))
        
        # Выбираем случайное сообщение для ответа, если есть сообщения
        reply_for = None
        if messages and random.choice([True, False]):
            reply_for = random.choice([m["id"] for m in messages])
  
        messages.append({
            "id": uuid.uuid4(),
            "sent_at": sent_at,
            "sent_by": random.choice(users_ids),
            "reply_for": reply_for,
            "seen_by": random.sample(users_ids, random.randint(1, len(users_ids)//2)),
            "text": lorem.sentence(),
        })
    return messages


def get_most_active_user(messages):
    """Возвращает ID пользователя, который написал больше всех сообщений"""
    user_message_count = Counter(msg["sent_by"] for msg in messages)
    most_active = user_message_count.most_common(1)[0]
    return most_active[0], most_active[1]


def get_most_replied_user(messages):
    """Возвращает ID пользователя, на сообщения которого больше всего отвечали"""
    # Считаем, сколько раз на сообщения каждого пользователя отвечали
    reply_count = defaultdict(int)
    
    # Создаем словарь для быстрого поиска автора сообщения по ID
    message_author = {msg["id"]: msg["sent_by"] for msg in messages}
    
    for msg in messages:
        if msg["reply_for"] and msg["reply_for"] in message_author:
            original_author = message_author[msg["reply_for"]]
            reply_count[original_author] += 1
    
    if not reply_count:
        return None, 0
    
    most_replied = max(reply_count.items(), key=lambda x: x[1])
    return most_replied[0], most_replied[1]


def get_users_with_most_seen_messages(messages):
    """Возвращает ID пользователей, сообщения которых видело больше всего уникальных пользователей"""
    # Для каждого пользователя вычисляем среднее значение уникальных зрителей на сообщение
    user_viewers_sum = defaultdict(int)  # сумма уникальных читателей по всем сообщениям
    user_messages_count = defaultdict(int)  # количество сообщений
    
    for msg in messages:
        unique_viewers = len(set(msg["seen_by"]))
        user_viewers_sum[msg["sent_by"]] += unique_viewers
        user_messages_count[msg["sent_by"]] += 1
    
    # Вычисляем среднее
    user_avg = {}
    for user_id in user_viewers_sum:
        user_avg[user_id] = round(user_viewers_sum[user_id] / user_messages_count[user_id], 3)
    
    # Сортируем по среднему значению
    sorted_users = sorted(user_avg.items(), key=lambda x: x[1], reverse=True)
    
    return [(user_id, avg) for user_id, avg in sorted_users]


def get_most_active_time_period(messages):
    """Определяет, когда больше всего сообщений: утром, днём или вечером"""
    time_periods = {
        "ночь (0-6)": 0,
        "утро (6-12)": 0,
        "день (12-18)": 0,
        "вечер (18-24)": 0
    }
    
    for msg in messages:
        hour = msg["sent_at"].hour
        if 0 <= hour < 6:
            time_periods["ночь (0-6)"] += 1
        elif 6 <= hour < 12:
            time_periods["утро (6-12)"] += 1
        elif 12 <= hour < 18:
            time_periods["день (12-18)"] += 1
        else:
            time_periods["вечер (18-24)"] += 1
    
    most_active = max(time_periods.items(), key=lambda x: x[1])
    return most_active[0], most_active[1], time_periods


def find_longest_threads(messages, top_n=5):
    """Находит самые длинные цепочки ответов и возвращает ID начальных сообщений"""
    # Строим граф ответов: для каждого сообщения храним список ответов на него
    replies_graph = defaultdict(list)
    message_lookup = {msg["id"]: msg for msg in messages}
    
    for msg in messages:
        if msg["reply_for"]:
            replies_graph[msg["reply_for"]].append(msg["id"])
    
    def count_thread_messages(start_msg_id):
        """Рекурсивно считает количество сообщений в треде"""
        total = 1  # Считаем текущее сообщение
        for reply_id in replies_graph[start_msg_id]:
            total += count_thread_messages(reply_id)
        return total
    
    # Считаем длину треда для каждого сообщения
    thread_lengths = {}
    for msg in messages:
        # Рассматриваем только сообщения, которые не являются ответами (начала тредов)
        # или все сообщения (по заданию нужно найти начала тредов)
        thread_lengths[msg["id"]] = count_thread_messages(msg["id"])
    
    # Сортируем по длине треда и берём топ-N
    sorted_threads = sorted(thread_lengths.items(), key=lambda x: x[1], reverse=True)
    
    return [(msg_id, length, message_lookup[msg_id]["text"][:50] + "...") 
            for msg_id, length in sorted_threads[:top_n]]


def analyze_chat(messages):
    """Основная функция анализа чата"""
    print("=" * 60)
    print("АНАЛИЗ ЧАТА")
    print("=" * 60)
    
    # Задача 1
    user_id, count = get_most_active_user(messages)
    print(f"1. Самый активный пользователь: ID {user_id} (написал {count} сообщений)")
    
    # Задача 2
    user_id, count = get_most_replied_user(messages)
    if user_id:
        print(f"2. Пользователь, на чьи сообщения больше всего отвечали: ID {user_id} (получил {count} ответов)")
    else:
        print("2. Нет сообщений с ответами")
    
    # Задача 3
    users_with_views = get_users_with_most_seen_messages(messages)
    print("3. Топ пользователей по количеству уникальных читателей:")
    for i, (user_id, viewers_count) in enumerate(users_with_views[:5], 1):
        print(f"   {i}. ID {user_id}: {viewers_count} уникальных читателей")
    
    # Задача 4
    period, count, all_periods = get_most_active_time_period(messages)
    print(f"4. Больше всего сообщений в {period}: {count} сообщений")
    print(f"   Распределение: {all_periods}")
    
    # Задача 5
    longest_threads = find_longest_threads(messages, top_n=5)
    print("5. Самые длинные треды (начальные сообщения):")
    for i, (msg_id, length, preview) in enumerate(longest_threads, 1):
        print(f"   {i}. ID: {msg_id}, длина: {length} сообщений")
        print(f"      Текст: \"{preview}\"")


if __name__ == "__main__":
    # Генерация истории чата
    print("Генерация истории чата...")
    messages = generate_chat_history()
    print(f"Сгенерировано {len(messages)} сообщений")
    print()
    
    # Анализ чата
    analyze_chat(messages)
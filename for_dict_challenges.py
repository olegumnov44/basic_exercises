# Задание 1
# Дан список учеников, нужно посчитать количество повторений каждого имени ученика
# Пример вывода:
# Вася: 1
# Маша: 2
# Петя: 2

students = [
    {'first_name': 'Вася'},
    {'first_name': 'Петя'},
    {'first_name': 'Маша'},
    {'first_name': 'Маша'},
    {'first_name': 'Петя'},
]

counts = {}
for student in students:
    name = student['first_name']
    if name in counts:
        counts[name] += 1
    else:
        counts[name] = 1

for name, count in counts.items():
    print(f"{name}: {count}")

# способ 2
from collections import Counter
counts = Counter(student['first_name'] for student in students)

for name, count in counts.items():
    print(f"{name}: {count}")
    

# Задание 2
# Дан список учеников, нужно вывести самое часто повторящееся имя
# Пример вывода:
# Самое частое имя среди учеников: Маша
students = [
    {'first_name': 'Вася'},
    {'first_name': 'Петя'},
    {'first_name': 'Маша'},
    {'first_name': 'Маша'},
    {'first_name': 'Оля'},
]

from collections import Counter
counts = Counter(student['first_name'] for student in students)
#most_common_name = counts.most_common(1)[0][0] # (1)-выборка списка из 1-го кортежа [0]-1-й в списке  [0]-1-й в кортеже
most_common_name = max(counts, key=counts.get)

print("Самое частое повторение среди учеников:", most_common_name)


# Задание 3
# Есть список учеников в нескольких классах, нужно вывести самое частое имя в каждом классе.
# Пример вывода:
# Самое частое имя в классе 1: Вася
# Самое частое имя в классе 2: Маша

school_students = [
    [  # это – первый класс
        {'first_name': 'Вася'},
        {'first_name': 'Вася'},
    ],
    [  # это – второй класс
        {'first_name': 'Маша'},
        {'first_name': 'Маша'},
        {'first_name': 'Оля'},
    ],
    [  # это – третий класс
        {'first_name': 'Женя'},
        {'first_name': 'Петя'},
        {'first_name': 'Женя'},
        {'first_name': 'Саша'},
    ],
]

from collections import Counter
for index, students in enumerate(school_students):
    counts = Counter(student['first_name'] for student in students)
    most_common_name = max(counts, key=counts.get)
    print(f"Самое частое имя в классе {index+1}:", most_common_name)

# Задание 4
# Для каждого класса нужно вывести количество девочек и мальчиков в нём.
# Пример вывода:
# Класс 2a: девочки 2, мальчики 0 
# Класс 2б: девочки 0, мальчики 2

school = [
    {'class': '2a', 'students': [{'first_name': 'Маша'}, {'first_name': 'Оля'}]},
    {'class': '2б', 'students': [{'first_name': 'Олег'}, {'first_name': 'Миша'}]},
    {'class': '2в', 'students': [{'first_name': 'Даша'}, {'first_name': 'Олег'}, {'first_name': 'Маша'}]},
]
is_male = {
    'Олег': True,
    'Маша': False,
    'Оля': False,
    'Миша': True,
    'Даша': False,
}

for class_info in school:
    girls_count = 0
    boys_count = 0
    for student in class_info['students']:
        name = student['first_name']
        if is_male.get(name):
            boys_count += 1
        else:  
            girls_count += 1
            
    print(f"Класс {class_info['class']}: девочки {girls_count}, мальчики {boys_count}")


# Задание 5
# По информации о учениках разных классов нужно найти класс, в котором больше всего девочек и больше всего мальчиков
# Пример вывода:
# Больше всего мальчиков в классе 3c
# Больше всего девочек в классе 2a

school = [
    {'class': '2a', 'students': [{'first_name': 'Маша'}, {'first_name': 'Оля'}]},
    {'class': '3c', 'students': [{'first_name': 'Олег'}, {'first_name': 'Миша'}]},
]
is_male = {
    'Маша': False,
    'Оля': False,
    'Олег': True,
    'Миша': True,
}

boys_in_class = {}
girls_in_class = {}
for class_info in school:
    class_name = class_info['class']
    girls_count = 0
    boys_count = 0
    for student in class_info['students']:
        name = student['first_name']
        if is_male.get(name):
            boys_count += 1
        else:  
            girls_count += 1
    
    boys_in_class[class_name] = boys_count
    girls_in_class[class_name] = girls_count

max_boys_class = max(boys_in_class, key=boys_in_class.get)
max_boys_count = boys_in_class[max_boys_class]

max_girls_class = max(girls_in_class, key=girls_in_class.get)
max_girls_count = girls_in_class[max_girls_class]

print(f"Больше всего мальчиков в классе {max_boys_class}")
print(f"Больше всего девочек в классе {max_girls_class}")
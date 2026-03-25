# Вывести последнюю букву в слове
word = 'Архангельск'
print(f"Последняя буква в слове 'Архангельск': '{word[-1]}'")


# Вывести количество букв "а" в слове
word = 'Архангельск'
print("Количество букв 'а' и 'А':", word.count('А') + word.count('а'))


# Вывести количество гласных букв в слове
word = 'Архангельск'
vowels = 'аАеЕёЁиИоОуУэыЫЭяЯ'
count = 0
for vowel in vowels:
    count += word.count(vowel)
    
print("Количество гласных букв в слове:", count)


# Вывести количество слов в предложении
sentence = 'Мы приехали в гости'
print("Количество слов в предложении:", len(sentence.split()))


# Вывести первую букву каждого слова на отдельной строке
sentence = 'Мы приехали в гости'
for word in sentence.split():
    print(word[0])


# Вывести усреднённую длину слова в предложении
sentence = 'Мы приехали в гости'
words = sentence.split()
count_words = len(words)
count_symbols = 0
for word in sentence.split():
    count_symbols += len(word)
    
print("Средняя длина слова:", count_symbols/count_words)
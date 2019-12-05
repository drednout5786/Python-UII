f = open('text.txt', 'r', encoding = 'utf-8')
txt = f.read()
print(txt)
f.close()

# 1) Методами строк очистить текст от знаков препинания
print("Задача 1")
punctuation = "!#$%&'()*+,-./:;<=>?@[\]^_`{|}~—«»"
for i in punctuation:
    txt = txt.replace(i, "")
print(txt)

# 2) Сформировать list со словами (split)
print("Задача 2")
txt_split = txt.split()
print(txt_split)

# 3) привести все слова к нижнему регистру (map)
print("Задача 3_1")
txt_map = list(map(lambda x:x.lower(), txt_split))
print(txt_map)

# 3) Получить из list пункта 3 dict, ключами которого являются слова, а значениями их количество появлений в тексте
print("Задача 3_2")
dict=set(txt_map)
dict_whole = {}
for element in dict:
    dict_whole[element]=txt_map.count(element)
print(dict_whole)

# 4) Вывести 5 наиболее часто встречающихся слов (sort), вывести количество разных слов в тексте (set);
print("Задача 4")
list_d=list(dict_whole.items())
list_d.sort(key=lambda i:i[1],reverse=True)
print("5 наиболее часто встречающихся слов: ", list_d[:5])

print("Количество разных слов в тексте: ", len(dict))

# 5) Выполнить light с условием: в пункте 2 дополнительно к приведению к нижнему регистру выполнить лемматизацию.
# Подробнее о процедуре лемматизации: https://pymorphy2.readthedocs.io/en/0.2/user/index.html
print("Задача 5")
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
words = []
for i in txt_map:
    words.append(morph.parse(i)[0].normal_form)
    
print(words)

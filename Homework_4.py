# 1. Напишите функцию (F): на вход список имен и целое число N; на выходе список длины N случайных имен из первого списка (могут повторяться, можно взять значения: количество имен 20, N = 100, рекомендуется использовать функцию random).
import random
list_name = ["Emily", "Emma", "Madison", "Olivia", "Hannah", "Abigail", "Isabella", "Ashley", "Samantha", "Elizabeth", "Alexis", "Sarah", "Grace", "Alyssa", "Sophia", "Lauren", "Brianna", "Kayla", "Natalie", "Anna"]
def random_names(ln, n):
    """
    :param ln - список имен
    :param n - целое число
    :return: список длины N случайных имен из первого списка
    """
    random_list = []
    len_ln = len(ln)
    if len_ln == 0:
        return random_list
    else:
        for i in range(n):
            random_i = random.randint(0, len_ln-1)
            random_list.append(ln[random_i])
        #print("Количество элементов в полученном списке: ", len(random_list))
        return random_list

print("Задача 1")
rn = random_names(list_name, 100)
print('Полученный список имен: ', rn)

# 2. Напишите функцию вывода самого частого имени из списка на выходе функции F.
from collections import Counter
def most_common_name(names):
    """
    :param names - список имен
    :return - самое частое имя из списка
    """
    if len(names) == 0:
        return 'Введенный список пуст.'
    count_names = Counter(names)
    #print(count_names)
    most_common = sorted(count_names, key=lambda x: x[1])
    #print("most_common", most_common)
    return most_common[0][0]

print("Задача 2")
item = most_common_name(rn)
print('Самое частое имя из списка: ', item)

# 3. Напишите функцию вывода самой редкой буквы, с которого начинаются имена в списке на выходе функции F.
def rarest_letter(names):
    """
    :param names - список имен
    :return - самая редкая буква, с которой начинаются имена в списке
    """
    if len(names) == 0:
        return 'Введенный список пуст.'
    else:
        letters_list = list(map(lambda x: x[0], names))
        #print("letters_list: ", letters_list)
        count_names = Counter(letters_list)
        #print("count_names:", count_names)
        most_common = count_names.most_common()[-1:]
        #print("most_common: ", most_common)
        return most_common[0]

print("Задача 3")
rl = rarest_letter(rn)
#print(type(rl), rl[0], rl[1])
print('Самая редкая буква, с которой начинаются имена в списке: ', rl[0])
# print("Она встречается", rl[1], "раз.")

# 4. В файле с логами найти дату самого позднего лога (по метке времени).
with open('log', 'r') as f:
    f = f.readlines()
    #print(f, '\n')

late_log = max(f, key=lambda x: x[:19])
print("Задача 4")
print('Дата самого позднего лога (по метке времени):', late_log[:19])


'''
Задача 1
Вывести на экран циклом пять строк из нулей, причем каждая строка должна быть пронумерована.
'''
print("Задача 1")
for i in range(1, 6):
    print(i, 0)
    i += 1

'''
Задача 2
Пользователь в цикле вводит 10 цифр. Найти количество введеных пользователем цифр 5.
'''
print("Задача 2")
count = 0
for i in range(1, 11):
    print('Введите цифру номер ', i, ': ', end='')
    num = input()
    while  len(num) != 1 or not num.isdigit():
        print(num, ' - не цифра')
        print('Введите цифру номер ', i, ': ', end = '')
        num = input()
    dig = int(num)
    if dig == 5: count += 1
print('Количество введеных пользователем цифр 5:', count)
'''
Задача 3
Найти сумму ряда чисел от 1 до 100. Полученный результат вывести на экран.
'''
print("Задача 3")
sum = 0
for i in range(1,101):
     sum+=i
print('Сумма ряда чисел от 1 до 100: ', sum)

'''
Задача 4
Найти произведение ряда чисел от 1 до 10. Полученный результат вывести на экран.
'''
print("Задача 4")
p = 1
for i in range(1,11):
     p*=i
print('Произведение ряда чисел от 1 до 100: ', p)
'''
Задача 5
Вывести цифры числа на каждой строчке.
'''
print("Задача 5")
integer_number = 5689
while integer_number>0:
    print(integer_number%10)
    integer_number = integer_number//10
'''
Задача 6
Найти сумму цифр числа.
'''
print("Задача 6")
integer_number = 123
print('Задано число: ', integer_number)
sum = 0
while integer_number>0:
    dig = integer_number%10
    sum+=dig
    integer_number = integer_number//10
print('Сумма цифр числа: ', sum)
'''
Задача 7
Найти произведение цифр числа.
'''
print("Задача 7")
integer_number = 234
print('Задано число: ', integer_number)
p = 1
while integer_number>0:
    dig = integer_number%10
    p*=dig
    integer_number = integer_number//10
print('Произведение цифр числа: ', p)

'''
Задача 8
Дать ответ на вопрос: есть ли среди цифр числа 5?
'''
print("Задача 8")
integer_number = 213553
print('Задано число: ', integer_number)
while integer_number>0:
    if integer_number%10 == 5:
        print('Число содержит цифру 5')
        break
    integer_number = integer_number//10
else: print('Число не содержит цифру 5')

'''
Задача 9
Найти максимальную цифру в числе
'''
print("Задача 9")
max = 0
num = int(input('Введите число: '))
while num > 0:
    if num%10 > max:
        max = num % 10
    else: num = num//10
print("Максимальная цифра в числе - ", max)
'''
Задача 10
Найти количество цифр 5 в числе
'''
print("Задача 10")
num = int(input('Введите число: '))
con = 0
while num > 0:
    if num%10 == 5:
        con +=1
    num = num//10
print('Количество цифр 5 в числе:', con)

from hwp_5 import divisor_master as dm

# 0) Воод числа
var = input('Введите натуральное число от 1 до 1000: ')
while True:
    if (var.isdigit() != True): print("Это не натуральное число.")
    elif (int(var) > 1000): print("Введенное число больше 1000.")
    else: break
    var = input('Введите натуральное число от 1 до 1000: ')
num = int (var)
print("Вы ввели число: ", num)

# 1) проверка числа на простоту (простые числа - это те числа у которых делители единица и они сами);
print("Задача 1")
print("Число =", num, "" if dm.is_prime(num) else "не", "является простым.")

# 2) выводит список всех делителей числа;
print("Задача 2")
print("Список всех делителей числа:", dm.dividers_list(num))

# 3) выводит самый большой простой делитель числа.
print("Задача 3")
print("Самый большой простой делитель числа:", dm.max_simple_dividers(num))

# 4) функция выводит каноническое разложение числа (https://zaochnik.com/spravochnik/matematika/delimost/razlozhenie-chisel-na-prostye-mnozhiteli/) на простые множители;
print("Задача 4")
print("Каноническое разложение числа на простые множители: ", dm.canonical_decomposition(num))

# 5)функция выводит самый большой делитель (не обязательно простой) числа.
print("Задача 5")
print("Самый большой (не обязательно простой) делитель числа:", dm.max_dividers(num))
import time
import psutil
import os

N = 1000000

# 1. Написать декоратор, замеряющий время выполнение декорируемой функции.
def show_time(f): # время выполнения декорируемой функции
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print("Начало выполнения: ", start_time)
        text = f(*args, **kwargs)
        end_time = time.time()
        print("Окончание выполнения: ", end_time)
        global duration_time
        duration_time = end_time - start_time
        print("Время выполнения: ", duration_time)
        return text
    return wrapper

# 2. Сравнить время создания генератора и списка с элементами: натуральные числа от 1 до 1000000 (создание объектов оформить в виде функций).
@show_time
# Создание списка с элементами: натуральные числа от 1 до 1000000
def list_creation_01(a,b):
    list_sq = []
    for i in range(a, b + 1): list_sq.append(i)
    return list_sq

@show_time
# Создание генератора с элементами: натуральные числа от 1 до 1000000
def generator_creation_01(a,b):
    for i in range(a, b+1):
        yield(i)

print("Задача 01: создание списка с элементами")
list_creation_01(1,N)
duration_time_list = duration_time

print("\nЗадача 02: создание генератора с элементами")
generator_creation_01(1,N)
duration_time_generator = duration_time

if duration_time_list > duration_time_generator:
    print('\nВЫВОД 1: Время создания листа больше времени создания генератора.\n')
else:
    print('\nВЫВОД 1: Время создания генератора больше времени создания листа.\n')

# 3. Написать декоратор, замеряющий объем оперативной памяти, потребляемый декорируемой функцией.
def get_memory_size():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss/1000000

def show_RAM_size(f):
    def wrapper(*args, **kwargs):
        mem_before = get_memory_size()
        print('Исп. память до вып. функции: ' + str(mem_before))
        result = f(*args, **kwargs)
        mem_after = get_memory_size()
        print('Исп. память после вып. функции: ' + str(mem_after))
        global RAM_size
        RAM_size = mem_after - mem_before
        print("Объем оперативной памяти использованный для выполнения функции: ", RAM_size)
        return result
    return wrapper

# 4. Сравнить объем оперативной памяти для функции создания генератора и функции создания списка с элементами: натуральные числа от 1 до 1000000.
@show_RAM_size
# Создание списка с элементами: натуральные числа от 1 до 1000000
def list_creation_02(a, b):
    list_sq = []
    for i in range(a, b + 1): list_sq.append(i)
    return list_sq

@show_RAM_size
# Создание генератора с элементами: натуральные числа от 1 до 1000000
def generator_creation_02(a,b):
    for i in range(a, b+1):
        yield(i)

print("Задача 001: создание списка с элементами")
list_creation_02(1,N)
RAM_size_list = RAM_size

print("\nЗадача 002: создание генератора с элементами")
generator_creation_02(1,N)
RAM_size_generator = RAM_size

if RAM_size_list > RAM_size_generator:
    print('\nВЫВОД 2: Объем оперативной памяти для создания листа больше объема памяти для создания генератора.\n')
else:
    print('\nВЫВОД 2: Объем оперативной памяти для  создания генератора больше объема памяти для создания листа.\n')


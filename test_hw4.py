from Homework_4 import random_names

# Чистая функция, это функция, которая:
# Является детерминированной; Недетерминированность функции — возможность возвращения функцией разных значений несмотря на то, что ей передаются на вход одинаковые значения входных аргументов.
# Не обладает побочными эффектами. Модифицировать значения глобальных переменных, осуществлять операции ввода-вывода, реагировать на исключительные ситуации, вызывая их обработчики.

def test_1_dirty_function(): # Проверка выдачи списка из 100 элементов
    list_name_test = ["Emily", "Emma", "Madison", "Olivia", "Hannah", "Abigail", "Isabella", "Ashley", "Samantha",
                 "Elizabeth"]
    list_len = 100
    assert len(random_names(list_name_test, list_len))==list_len

def test_2_dirty_function(): # Проверка на детерминированность: возвращение функцией разных значений несмотря на то, что ей передаются на вход одинаковые значения входных аргументов
    list_name_test = ["Emily", "Emma", "Madison", "Olivia", "Hannah", "Abigail", "Isabella", "Ashley", "Samantha",
                 "Elizabeth", "Alexis"]
    assert random_names(list_name_test, 100) == random_names(list_name_test, 100)
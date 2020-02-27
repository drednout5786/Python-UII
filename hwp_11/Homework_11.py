import pandas as pd
import numpy as np
from statsmodels.stats.weightstats import zconfint
from scipy import stats
from statistics import mode

class EBM: # Доказа́тельная медици́на, англ. evidence-based medicine (EBM)

    def __init__(self, file, p_val): # Инициализация
        self.file = file
        self.p_val = p_val
        self.num_var = 1
        self.v = "N1"

    def __str__(self): # К уроку 11 1 номер
        return f'class EBM: ({self.file}, {self.p_val}, {self.v})'

    def __del__(self): # К уроку 11 2 номер
        del self.file
        del self.p_val
        del self.num_var
        del self.v

    def __getitem__(self, key): # К уроку 11 3 номер
        self.v = key
        return  self.v

    def __getstate__(self): # К уроку 11 4 номер
        return self.v

    def __setstate__(self, state): # К уроку 11 5 номер
        self.v = state

    def __eq__(self, other): # == # К уроку 11 6 номер
        if isinstance(other, EBM):
            return (self.v == other.v)
        if isinstance(other, str):
            return (self.v == other)

    def __ne__(self, other): # != # К уроку 11 7 номер
        if isinstance(other, EBM):
            return (self.v != other.v)
        if isinstance(other, str):
            return (self.v != other)

    def __add__(self, other): # + # К уроку 11 8 номер
        self.__scale_t = self.scale_type(self.v)
        other.__scale_t = other.scale_type(other.v)
        return self.normality_test(self.v) == other.normality_test(other.v)


    def __mul__(self, other): # * # К уроку 11 9 номер
        self.__scale_t = self.scale_type(self.v)
        other.__scale_t = other.scale_type(other.v)
        return (self.normality_test(self.v) == 1) and (other.normality_test(other.v) == 1)

    def __len__(self): # len # К уроку 11 10 номер
        return len(self.df.columns.tolist())

    def get_data_xlsx(self): # Считывание файла с данными
        try:
            self.df = pd.read_excel(self.file)
            if (self.df.empty):
                print("Файл '{}' пуст".format(self.file))
                return False
            else:
                print("Файл '{}' загружен.".format(self.file))
                print("Структура файла: \n", self.df.head(5))
                return True
        except (IOError, Exception) as e:
            print(e)
            #raise Exception(f'castom error{e}')
            return False

    def get_file_info(self): # Краткое описание файла
        print("\nКраткое описание файла:")
        print("Количество строк: {} Количество столбцов: {}".format(self.df.shape[0],  self.df.shape[1]))
        #print(f'Количество строк: {self.df.shape[0]} Количество столбцов: {self.df.shape[1]}')

    def get_column_name(self): # Вопрос пользователю - какой столбец анализируем?
        self.customer_choice = input('Введите название столбца, данные из которого хотите проанализировать?: {} \n'
                                     'или 0, чтобы отказаться от выбора и окончить выполнение анализа.\n'.format(self.df.columns.tolist()))
        while (self.customer_choice != "0") and (self.customer_choice not in list(self.df)):
            print("Вы выбрали столбец: {}. Его нет в списке столбцов.".format(self.customer_choice))
            self.customer_choice = input('Введите название столбца, данные из которого хотите проанализировать?: {} \n'
                                         'или 0, чтобы отказаться от выбора и окончить выполнение анализа.\n'.format(self.df.columns.tolist()))
        return self.customer_choice

    def scale_type(self, var): # Определение типа шкалы переменной
        if self.df[var].dtype in ['int8', 'int16', 'int32', 'int64']:
            # print("Данные распределены по порядковой шкале.")
            self.__scale_t = 'порядковая'
        elif self.df[var].dtype in ['float32', 'float64']:
            # print("Данные распределены по количественной шкале.")
            self.__scale_t = 'количественная'
        elif self.df[var].dtype in ['O']:
            if type(self.df[var][0]) == np.str:
                # print("Данные распределены по номинальной (категориальной) шкале.")
                self.__scale_t = 'номинальная'
            else:
                # print("Данные распределены по неопределенной шкале.")
                self.__scale_t = 'не определен'
        else:
            # print("Данные распределены по неопределенной шкале.")
            self.__scale_t = 'не определен'
        return self.__scale_t

    def describe_value(self): # Краткое описание переменной
        print("Анализ - Краткое описание переменной")
        if (self.__scale_t == 'порядковая') or (self.__scale_t == 'количественная'):
            print(self.df[self.customer_choice].describe())
        else:
            print(self.df[self.customer_choice].groupby(self.df[self.customer_choice]).count())

    def normality_test(self, var): # Проверка на нормальность распределения
        if self.num_var == "2" :
            self.__scale_t = self.scale_type(var)

        if (self.__scale_t == 'порядковая') or (self.__scale_t == 'количественная'):
            SW = stats.shapiro(self.df[var])
            if SW[1] > self.p_val:
                self.__norm = 1
                print("Тест Шапиро-Уилка на нормальность распределения: W = {:.6}, p = {:f}. Вывод: распределение нормально.".format(SW[0], SW[1]))
                print('Среднее: {:.4} и 95% доверительный интервал: [{:.4}, {:.4}]'.format(np.mean(self.df[var], axis = 0), zconfint(self.df[var])[0],
                                                                           zconfint(self.df[var])[1]))
            else:
                self.__norm = 0
                print("Тест Шапиро-Уилка на нормальность распределения: W = {:.6}, p = {:f}. Вывод: распределение НЕ нормально.".format(SW[0], SW[1]))
        else:
            print("Данные не имеют количественной природы. Проверка на нормальность не требуется.")
            self.__norm = -1
        return self.__norm

    def typical_value(self): # Расчет типичного значения выборки
        if (self.__scale_t == 'порядковая') or (self.__scale_t == 'количественная'):
            if self.__norm == 0:
                q25, q50, q75 = np.percentile(self.df[self.customer_choice], [25, 50, 75])
                print("Типичное значение выборки Медиана [Q1; Q3] = {} [{}; {}].".format(round(q50, 2), round(q25, 2), round(q75, 2)))
            else:
                print("Типичное значение выборки Среднее ± стандартное отклонение = {} ± {}.".format(round(np.mean(self.df[self.customer_choice], axis = 0), 2),
                                                                                                    round(np.std(self.df[self.customer_choice], axis = 0), 2)))
        elif self.__scale_t == 'номинальная':
            print("Типичное значение выборки Мода = {}.".format(mode(self.df[self.customer_choice])))

if __name__ == '__main__':
    EBM_easy_1 = EBM("./для ЕВ_1.xlsx", 0.05)
    EBM_easy_2 = EBM("./для ЕВ_2.xlsx", 0.05)

    if (EBM_easy_1.get_data_xlsx()) and (EBM_easy_2.get_data_xlsx()): # Считывание файла с данными
        print("**EBM_easy_1 = ", EBM_easy_1) # Печать класса
        print("**Проверка на равенство классов: ", EBM_easy_1 == EBM_easy_2) # Проверка 2 классов на ==
        print("**Проверка на равенство с переменной: ", EBM_easy_1 == "N2") # Проверка класса и переменной на !=
        print("**Проверка на неравенство классов: ", EBM_easy_1 != EBM_easy_2) # Проверка 2 классов на !=
        print("**Проверка на неравенство с переменной: ", EBM_easy_1 != "N2") # Проверка класса и переменной на ==
        print("**Сложение классов: ", EBM_easy_1 + EBM_easy_2) # Один из классов должен иметь нормальное распределение
        print("**Умножение классов: ", EBM_easy_1 * EBM_easy_2) # Оба класса должны иметь нормальное распределение
        print("**Длина класса: ", len(EBM_easy_1))  # Количество переменных в классе, доступных для анализа

        print('\nРабота программы по анализу данных закончена!')

    # if EBM_easy.get_data_xlsx(): # Считывание файла с данными
    #     EBM_easy.get_file_info() # Краткое описание файла
    #
    #     while (EBM_easy.get_column_name() != '0'): # Вопрос пользователю - какой столбец анализируем?
    #         EBM_easy.scale_type(EBM_easy.customer_choice) # Определение типа шкалы переменной
    #         EBM_easy.describe_value()  # Краткое описание переменной
    #         EBM_easy.normality_test(EBM_easy.customer_choice)  # Проверка на нормальность распределения
    #         EBM_easy.typical_value()  # Расчет типичного значения выборки
    #     print('\nРабота программы по анализу данных закончена!')
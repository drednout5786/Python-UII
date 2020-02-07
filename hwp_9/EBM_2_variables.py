from Les_9_1 import EBM
import numpy as np
from scipy import stats

# d = EBM(2, "./для ЕВ.xlsx")

class EMB_2_var(EBM): # Доказа́тельная медици́на, англ. evidence-based medicine (EBM)
    '''
    Допишем функции анализа 2 переменных одновременно.
    num_var 1: анализ одной переменной
    num_var 2: анализ 2-х переменных одновременно
    функции по статистике: https://docs.scipy.org/doc/scipy-0.14.0/reference/stats.html
    '''

    # def __init__(self, file): # лишняя сущность
    #     super().__init__(file)

    def get_amount_var(self): # Вопрос пользователю - сколько столбцов анализируем?
        self.num_var = input('\nВведите количество столбцов для анализа?: 1 или 2.'
                             'Чтобы отказаться от выбора и окончить выполнение анализа нажмите 0.\n')
        while (self.num_var != "0") and (self.num_var not in ['1', '2']) :
            print("Вы выбрали неверное количество столбцов:", self.num_var, ". Оно должно быть 1 или 2.")
            self.num_var = input('\nВведите количество столбцов для анализа?: 1 или 2.'
                                 'Чтобы отказаться от выбора и окончить выполнение анализа нажмите 0.\n')
        return self.num_var

    def scale_type_2(self):  # Определение типа шкалы переменной
        self.__scale_t1 = self.scale_type(self.customer_choice_1)
        self.__scale_t2 = self.scale_type(self.customer_choice_2)

    def normality_test_2(self): # Проверка на нормальность распределения
        print(self.customer_choice_1, end=":  \t")
        self.__norm_1 = self.normality_test(self.customer_choice_1)
        print(self.customer_choice_2, end=":  \t")
        self.__norm_2 = self.normality_test(self.customer_choice_2)

        if (self.__norm_1 == -1) or (self.__norm_2 == -1):
            self.__norm = -1
        elif (self.__norm_1 == 0) or (self.__norm_2 == 0):
            self.__norm = 0
        else:
            self.__norm = 1

    def correlation(self): # Проверка на наличие корреляции
        c = 1
        if self.__norm == 1:
            print("\nПроверка на наличие корреляции при нормальном распределении.")
            coef, p_value = stats.pearsonr(self.df[self.customer_choice_1], self.df[
                self.customer_choice_2])  # Calculates a Pearson correlation coefficient and the p-value for testing non-correlation
            print("Коэффициент корреляции Пирсона: R = {} P-value = : {}".format(coef, p_value))
        elif self.__norm == 0:
            print("\nПроверка на наличие корреляции при ненормальном распределении.")
            coef, p_value = stats.spearmanr(self.df[self.customer_choice_1], self.df[
                self.customer_choice_2])  # Calculates a Spearman rank-order correlation coefficient and the p-value to test for non-correlation
            print("Коэффициент корреляции Спирмена: Rs = {} P-value = : {}".format(coef, p_value))
        else:
            print("Проверка на наличие корреляции не возможно. Тип данных одной или обеих переменных не количественный.")
            c = 0

        if c == 1:
            if p_value > self.p_val:
                print("Вывод: Корреляция между {} и {} статистически не значима при p<0.05".format(self.customer_choice_1,
                                                                                                   self.customer_choice_2))
            else:
                print("Вывод: Корреляция между {} и {} статистически значима при p<0.05".format(self.customer_choice_1,
                                                                                                self.customer_choice_2))
                if coef > 0:
                    direction = "положительной"
                else:
                    direction = "отрицательной"

                if abs(coef) < 0.3:
                    closeness = "слабой"
                elif abs(coef) < 0.7:
                    closeness = "умеренной"
                else:
                    closeness = "сильной"
                print("Выявленная связь по направлению является {}. По тесноте - {}.".format(direction, closeness))

    def wilcoxon_t(self):  # для не нормального распределения: Критерий Вилкоксона проверяет нулевую гипотезу о том, что две связанных выборки происходят из одного и того же распределения.
                           # для нормального распределения: t-критерий для двух связанных выборок. Проверяет имеют ли выборки идентичные средние значения.
        w = 1
        if self.__norm == 1:
            t_statistic, p_value = stats.ttest_rel(self.df[self.customer_choice_1], self.df[self.customer_choice_2])
            print("\nt-критерий Стьюдента: Т = ", t_statistic, " P-value = :", p_value)  # Results
        elif self.__norm == 0:
            if len(self.df[self.customer_choice_1]) > 20 :
                z_statistic, p_value = stats.wilcoxon(self.df[self.customer_choice_1], self.df[self.customer_choice_2])
                print("\nКритерий Вилкоксона: W = ", z_statistic, " P-value = :", p_value)  # Results
            else:
                print("Проверка по критерию Вилксона не возможна, т.к. выборка содержит менее 20 значений.")
                w = 0
        else:
            print("Проверка по критерию Вилксона/Т-Стьюдента не возможна. Тип данных одной или обеих переменных не количественный.")
            w = 0

        if w == 1:
            if p_value > self.p_val:
                print("Вывод: Изменения показателя {} => {} статистически не значимы при p<0.05".format(self.customer_choice_1,
                                                                                                        self.customer_choice_2))
            else:
                print("Вывод: Изменения показателя {} => {} статистически значимы при p<0.05".format(self.customer_choice_1,
                                                                                                     self.customer_choice_2))
if __name__ == '__main__':
    EBM_complex = EMB_2_var("./для ЕВ.xlsx", 0.05)

    if EBM_complex.get_data_xlsx():# Считывание файла с данными
        EBM_complex.get_file_info()# Краткое описание файла

    while (EBM_complex.get_amount_var() != '0') :  # Вопрос пользователю - сколько столбцов анализируем?
        if EBM_complex.num_var == '1':
            while (EBM_complex.get_column_name() != '0'):  # Вопрос пользователю - какой столбец анализируем?
                print("Выполнен анализ переменной: {}.".format(EBM_complex.customer_choice))
                EBM_complex.scale_type(EBM_complex.customer_choice)  # Определение типа шкалы переменной
                EBM_complex.describe_value()  # Краткое описание переменной
                EBM_complex.normality_test(EBM_complex.customer_choice)  # Проверка на нормальность распределения
                EBM_complex.typical_value()  # Расчет типичного значения выборки
                break
        else:
            EBM_complex.customer_choice_1 = EBM_complex.get_column_name() # Вопрос пользователю - какой столбец анализируем?
            EBM_complex.customer_choice_2 = EBM_complex.get_column_name()
            while (EBM_complex.customer_choice_1 != '0') and (EBM_complex.customer_choice_2 != '0'):
                # print("Анализ 2 переменных:")
                EBM_complex.scale_type_2()  # Определение типа шкалы переменной
                EBM_complex.normality_test_2()  # Проверка на нормальность распределения
                EBM_complex.correlation() # Проверка на наличие корреляции
                EBM_complex.wilcoxon_t()  # Критерий Вилкоксона / Критерий Т-Стьюдента
                # print("self._norm = ", EBM_complex.__norm) # проверка доступности скрытого значения EBM_complex.__norm
                break

    print('\nРабота программы по анализу данных закончена!')
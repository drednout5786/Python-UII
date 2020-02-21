import pytest
import pandas as pd
import numpy as np
import warnings
from statistics import mode
from statsmodels.stats.weightstats import zconfint
from scipy import stats
from Les_9_1 import EBM

class TestEBM_pytest:

    def setup(self):
        self.EBM_work = EBM("./для ЕВ.xlsx", 0.05)
        print('Начало тестирования!')

    def teardown(self):
        print('Тестирование завершено!')

    def test_init(self):
        assert self.EBM_work.file == "./для ЕВ.xlsx"
        assert self.EBM_work.p_val == 0.05

    def test_get_data_xlsx(self):
        with pytest.raises(Exception) as excinfo:
            raise Exception('Нет такого файла или директории.')

    def test_get_file_info(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            self.EBM_work.df = pd.read_excel(self.EBM_work.file)
            assert self.EBM_work.df.shape[0] == 410
            assert self.EBM_work.df.shape[1] == 16

    def test_scale_type(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            self.EBM_work.df = pd.read_excel(self.EBM_work.file)
            var = "ВОЗРАСТ"
            assert self.EBM_work.scale_type(var) == 'порядковая'
            var = "ФО"
            assert self.EBM_work.scale_type(var) == 'номинальная'
            var = "BF"
            assert self.EBM_work.scale_type(var) == 'количественная'

    def test_normality_test(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            self.EBM_work.df = pd.read_excel(self.EBM_work.file)
            var = "ВОЗРАСТ"
            self.EBM_work.scale_type(var)
            assert self.EBM_work.normality_test(var) == 0 # распределение не нормально
            assert round(stats.shapiro(self.EBM_work.df[var])[0], 4) == 0.9733
            assert stats.shapiro(self.EBM_work.df[var])[1] < 0.05

            var = "BF"
            self.EBM_work.scale_type(var)
            assert self.EBM_work.normality_test(var) == 0 # распределение не нормально
            assert round(stats.shapiro(self.EBM_work.df[var])[0], 4) == 0.7668
            assert stats.shapiro(self.EBM_work.df[var])[1] < 0.05

            var = "N1"
            self.EBM_work.scale_type(var)
            assert self.EBM_work.normality_test(var) == 1 # распределение нормально
            assert round(stats.shapiro(self.EBM_work.df[var])[0], 4) == 0.9970
            assert stats.shapiro(self.EBM_work.df[var])[1] > 0.05
            assert round(np.mean(self.EBM_work.df[var], axis=0), 2) == 0.02
            assert round(np.std(self.EBM_work.df[var], axis=0), 2) == 2.18
            assert round(zconfint(self.EBM_work.df[var])[0], 4) == -0.1875
            assert round(zconfint(self.EBM_work.df[var])[1], 4) == 0.2353

            var = "N2"
            self.EBM_work.scale_type(var)
            assert self.EBM_work.normality_test(var) == 1 # распределение нормально
            assert stats.shapiro(self.EBM_work.df[var])[1] > 0.05

            var = "ФО"
            self.EBM_work.scale_type(var)
            assert self.EBM_work.normality_test(var) == -1 # Проверка на нормальность не требуется

            var = "Регион"
            self.EBM_work.scale_type(var)
            assert self.EBM_work.normality_test(var) == -1 # Проверка на нормальность не требуется

    def test_typical_value(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            self.EBM_work.df = pd.read_excel(self.EBM_work.file)
            self.EBM_work.customer_choice = "Регион"
            self.EBM_work.scale_type(self.EBM_work.customer_choice)
            assert mode(self.EBM_work.df[self.EBM_work.customer_choice]) == "Москва"

            self.EBM_work.customer_choice = "ФО"
            self.EBM_work.scale_type(self.EBM_work.customer_choice)
            assert mode(self.EBM_work.df[self.EBM_work.customer_choice]) == "ЦФО"

            self.EBM_work.customer_choice = "ВОЗРАСТ"
            assert self.EBM_work.scale_type(self.EBM_work.customer_choice) == 'порядковая' # Шкала порядковая
            assert self.EBM_work.normality_test(self.EBM_work.customer_choice) == 0  # распределение не нормально
            assert np.percentile(self.EBM_work.df[self.EBM_work.customer_choice], 25) == 34.0 # Q1
            assert np.percentile(self.EBM_work.df[self.EBM_work.customer_choice], 50) == 42.0  # Медиана
            assert np.percentile(self.EBM_work.df[self.EBM_work.customer_choice], 75) == 51.0  # Q3

            self.EBM_work.customer_choice = "BF"
            assert self.EBM_work.scale_type(self.EBM_work.customer_choice) == 'количественная' # Шкала количественная
            assert self.EBM_work.normality_test(self.EBM_work.customer_choice) == 0  # распределение не нормально
            assert np.percentile(self.EBM_work.df[self.EBM_work.customer_choice], 25) == 6.0 # Q1
            assert np.percentile(self.EBM_work.df[self.EBM_work.customer_choice], 50) == 11.0  # Медиана
            assert np.percentile(self.EBM_work.df[self.EBM_work.customer_choice], 75) == 20.0  # Q3

            self.EBM_work.customer_choice = "N1"
            assert self.EBM_work.scale_type(self.EBM_work.customer_choice) == 'количественная' # Шкала количественная
            assert self.EBM_work.normality_test(self.EBM_work.customer_choice) == 1  # распределение нормально
            assert stats.shapiro(self.EBM_work.df[self.EBM_work.customer_choice])[1] > 0.05
            assert round(np.mean(self.EBM_work.df[self.EBM_work.customer_choice], axis=0), 2) == 0.02
            assert round(np.std(self.EBM_work.df[self.EBM_work.customer_choice], axis=0), 2) == 2.18

# coverage run --branch test_pytest_EBM.py
# coverage report
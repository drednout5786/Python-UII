import unittest
import pandas as pd
import warnings
from Les_9_1 import EBM

class TestEBM_unittest (unittest.TestCase):

    def setUp(self):
        print('Начало тестирования!')
        self.EBM_work = EBM("./для ЕВ.xlsx", 0.05)

    def tearDown(self):
        # обычно происходит освобождение кэша:
        del self.EBM_work
        print('Тестирование завершено! Кэш освобожден.')

    def test_init(self):
        self.assertEqual(self.EBM_work.file, "./для ЕВ.xlsx")
        self.assertFalse(self.EBM_work.p_val > 0.05)

    def test_get_data_xlsx(self):
        with self.assertRaises(Exception) as excinfo:
            raise Exception('Нет такого файла или директории.')

    def test_get_file_info(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            self.EBM_work.df = pd.read_excel(self.EBM_work.file)
            self.assertTrue(self.EBM_work.df.shape[0] == 410)
            self.assertTrue(self.EBM_work.df.shape[1] == 16)

    def test_scale_type(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            self.EBM_work.df = pd.read_excel(self.EBM_work.file)
            var = "ВОЗРАСТ"
            self.assertTrue(self.EBM_work.scale_type(var) == 'порядковая')
            var = "ФО"
            self.assertTrue(self.EBM_work.scale_type(var) == 'номинальная')
            var = "BF"
            self.assertTrue(self.EBM_work.scale_type(var) == 'количественная')

    def test_normality_test(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            self.EBM_work.df = pd.read_excel(self.EBM_work.file)
            var = "ВОЗРАСТ"
            self.EBM_work.scale_type(var)
            self.assertTrue(self.EBM_work.normality_test(var) == 0)
            self.assertTrue(round(stats.shapiro(self.EBM_work.df[var])[0], 4) == 0.9733)
            self.assertTrue(stats.shapiro(self.EBM_work.df[var])[1] < 0.05)
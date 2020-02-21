import pytest
import pandas as pd
import warnings
from Les_9_1_bez_hidden import EBM

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

    def test_scale_type(self): # Дмитрий, вот этот тест не могу пройти.
        var = "ВОЗРАСТ"
        assert self.scale_t == 'номинальная'
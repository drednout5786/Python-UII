from divisor_master import *

# Тестирование функции is_prime
def test_is_prime():
    n = 47
    assert is_prime(n) == True
    n = 123
    assert is_prime(n) == False
    n = 999
    assert is_prime(n) == False
    n = 568
    assert is_prime(n) == False
    n = 659
    assert is_prime(n) == True

# Тестирование функции dividers_list
def test_dividers_list():
    n = 47
    assert dividers_list(n) == [1, 47]
    n = 123
    assert dividers_list(n) == [1, 3, 41, 123]
    n = 999
    assert dividers_list(n) == [1, 3, 9, 27, 37, 111, 333, 999]
    n = 568
    assert dividers_list(n) == [1, 2, 4, 8, 71, 142, 284, 568]
    n = 659
    assert dividers_list(n) == [1, 659]

# Тестирование функции max_simple_dividers
def test_max_simple_dividers():
    n = 47
    assert max_simple_dividers(n) == 47
    n = 123
    assert max_simple_dividers(n) == 41
    n = 999
    assert max_simple_dividers(n) == 37
    n = 568
    assert max_simple_dividers(n) == 71
    n = 659
    assert max_simple_dividers(n) == 659

# Тестирование функции canonical_decomposition
def test_canonical_decomposition():
    n = 47
    assert canonical_decomposition(n) == "47"
    n = 123
    assert canonical_decomposition(n) == "3*41"
    n = 999
    assert canonical_decomposition(n) == "3*3*3*37"
    n = 568
    assert canonical_decomposition(n) == "2*2*2*71"
    n = 659
    assert canonical_decomposition(n) == "659"

# Тестирование функции max_dividers
def test_max_dividers():
    n = 47
    assert max_dividers(n) == 47
    n = 123
    assert max_dividers(n) == 123
    n = 999
    assert max_dividers(n) == 999
    n = 568
    assert max_dividers(n) == 568
    n = 659
    assert max_dividers(n) == 659

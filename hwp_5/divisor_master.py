def is_prime(a):
    """
    :param a: число от 1 до 1000
    :return: простое или не простое число (True/False)
    """
    if a % 2 == 0:
        return a == 2
    d = 3
    while d * d <= a and a % d != 0:
        d += 2
    return d * d > a

def dividers_list(a):
    """
    :param a: число от 1 до 1000
    :return: список делителей числа
    """
    div_list = []
    for i in range(1, a + 1):
        if a % i == 0: div_list.append(i)
    return div_list

def simple_dividers(a):
    """
    :param a: число от 1 до 1000
    :return: список простых делителей числа
    """
    d_list = dividers_list(a)
    smpl_div_list = []
    l = len(d_list)
    for i in range(l):
        if is_prime(d_list[i]):
            smpl_div_list.append(d_list[i])
    return smpl_div_list

def max_simple_dividers(a):
    """
    :param a: число от 1 до 1000
    :return: самый большой простой делитель числа
    """
    return max(simple_dividers(a))

def max_dividers(a):
    """
    :param a: число от 1 до 1000
    :return: самый большой делитель (не обязательно простой) числа
    """
    return max(dividers_list(a))

def canonical_decomposition(a):
    """
    :param a: число от 1 до 1000
    :return: каноническое разложение числа на простые множители
    """
    a_begin = a
    sd = simple_dividers(a)
    lsd = len(sd)
#    print("sd = ", sd)
    con_dec = []
#    print("con_dec = ", con_dec)
    for i in range(1, lsd):
        while a_begin % sd[i] == 0:
            con_dec.append(sd[i])
            a_begin = a_begin/sd[i]
    lcd = len(con_dec)
    con_dec_txt = str(con_dec[0])
    for i in range(1, lcd):
        con_dec_txt = "{}*{}".format(con_dec_txt, con_dec[i])
    return con_dec_txt
# LIGHT:
# Необходимо выбрать сайт с однородно-повторяющейся информацией (отзывы о чем-то, описание объектов, резюме, вакансии и т.д.)
# и выполнить парсинг однородных данных с помощью библиотеки BeutifullSoup. Ответом будет являться csv файл, содержащий не менее 3х столбцов. Например, модель телефона, отзыв, дата отзыва.
#
# PRO:
# Выполнить задание LIGHT, но данные собирать не менее, чем с 2х различных источников. Особое внимание уделить приведению
# информации с различных источников к одному формату. Ответом также должен являться один csv файл.

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

URL = 'https://vuzopedia.ru/spec/region/city/59/91/vuzy'
# https://vuzoteka.ru/вузы/Прикладная-информатика-09-03-03
# https://vuzopedia.ru/spec/region/city/59/91/vuzy

pattern1 = r'от \d{5,6}'
pattern2 = r'Бюджетот \d{1,3}'
pattern3 = r'\d{1,3} местколичество бюджетных'
pattern4 = r'Платноеот \d{1,3}'
pattern5 = r'\d{1,3} местколичество платных'
pattern6 = r'Очная'
pattern7 = r'Очно-заочная'
pattern8 = r'Заочная'
pattern9 = r'Дистанционная'

vuz_list = [] # список вузов
cost_list = [] # список стоимости обучения
budjet_ball_list = [] # список проходной балл на бюджет
budjet_mest_list = [] # список количество мест на бюджет
dogovor_ball_list = [] # список проходной балл на платное
dogovor_mest_list = [] # список количество мест на платное
o4_fo_list = [] # список очная форма обучения
oz_fo_list = [] # список очно-заочная форма обучения
za_fo_list = [] # список заочная форма обучения
di_fo_list = [] # список дистанционная форма обучения

for page in range(10): # Выгрузим 10 страниц
    params = {'per_page':'10', 'page':page}
    response = requests.get(URL, params=params)
    # print(response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')

    lines = soup.find_all('div', class_ = 'itemVuzTitle')
    # print(page, 'itemVuzTitle = ', len(lines))
    for line in lines:
        # print(line.text)
        line_str = str(line.text).replace('\n', '')
        vuz_list.append(line_str.strip())  # заполняем вузами список вузов
    # print(str(vuz_list))
    # print ("Len lines = ", len(lines))

    lines = soup.find_all('div', class_ = 'itemSpecAll')
    # print ("Len costs = ", len(costs))

    for line in lines:
        # print(line.text)
        txt_str = str(line.text)  # преобразуем line.text в строку
        costs_all = str(re.findall(pattern1, txt_str))  # ищем стоимость обучения по шаблону
        cost_list.append(costs_all[5:(len(costs_all)-2)])  # заполняем ценами

        budjet_ball_all = str(re.findall(pattern2, txt_str))  # ищем проходной балл на бюджет по шаблону
        budjet_ball_list.append(budjet_ball_all[11:(len(budjet_ball_all)-2)])  # заполняем баллами

        budjet_mest_all = str(re.findall(pattern3, txt_str))  # ищем количество мест на бюджет
        budjet_mest_list.append(budjet_mest_all[2:-27])  # заполняем местами

        dogovor_ball_all = str(re.findall(pattern4, txt_str))  # ищем проходной балл на платное по шаблону
        dogovor_ball_list.append(dogovor_ball_all[12:(len(dogovor_ball_all)-2)])  # заполняем баллами

        dogovor_mest_all = str(re.findall(pattern5, txt_str))  # ищем количество мест на платное
        dogovor_mest_list.append(dogovor_mest_all[2:-25])  # заполняем местами

        o4_fo = str(re.findall(pattern6, txt_str))
        # print(o4_fo)
        # print("len o4_fo= ", len(o4_fo))
        if len(o4_fo) == 9: o4_fo_list.append("Есть")
        else: o4_fo_list.append("Нет")

        oz_fo = str(re.findall(pattern7, txt_str))
        if len(oz_fo) == 16: oz_fo_list.append("Есть")
        else: oz_fo_list.append("Нет")

        za_fo = str(re.findall(pattern8, txt_str))
        if len(za_fo) == 11: za_fo_list.append("Есть")
        else: za_fo_list.append("Нет")

        di_fo = str(re.findall(pattern9, txt_str))
        if len(di_fo) == 17: di_fo_list.append("Есть")
        else: di_fo_list.append("Нет")

# Формируем DataFrame
df = pd.DataFrame({
    'ВУЗ': vuz_list,
    'Стоимость': cost_list,
    'Бюджет балл': budjet_ball_list,
    'Бюджет мест': budjet_mest_list,
    'Договор балл': dogovor_ball_list,
    'Договор мест': dogovor_mest_list,
    'Очная форма обучения': o4_fo_list,
    'Очно-заочная форма обучения': oz_fo_list,
    'Заочная форма обучения': za_fo_list,
    'Дистанционная форма обучения': di_fo_list
})
df['Специальность'] = '09.03.03'
df['Сайт'] = 'vuzopedia.ru'
# print(df)

df.to_csv('df_1.csv') # создаем csv










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

pattern1 = r'места  Б (\d{1,3}|–) Д (\d{1,3}|–)'
pattern2 = r'\d{1,3}'
pattern3 = r'баллы егэ  Б (\d{1,3}|–) Д (\d{1,3}|–)'
pattern4 = r'стоимость   \d{1,3} \d{3}'
pattern5 = r'  Б – '

def budjet_dogovor(pattern):
    search_pat = str(re.search(pattern, txt_str))
    # print(search_pat)
    budjet = 0
    dogovor = 0
    search_pat_ = re.findall(pattern2, search_pat)
    # print(search_pat_)
    if len(search_pat_) == 4:
        budjet = search_pat_[2]
        dogovor = search_pat_[3]
    elif len(search_pat_) == 3:
        search_pat_5 = re.findall(pattern5, search_pat)
        # print(len(search_pat_5), search_pat_5)
        if len(search_pat_5)>0:
            budjet = 0
            dogovor = search_pat_[2]
        else:
            budjet = search_pat_[2]
            dogovor = 0
    return budjet, dogovor
# additional_proverka('/заочное-обучение')
def additional_proverka(pattern_fo):
    # проверяем заочные отделения вузов
    URL_za = URL+pattern_fo
    # print(URL_za)
    for page in range(33): # Выгрузим 33 страниц
        params = {'per_page':'10', 'page':page}
        response = requests.get(URL_za, params=params)
        # print(response.status_code)
        soup = BeautifulSoup(response.text, 'html.parser')
        lines = soup.find_all('div', class_='institute-row')
        # print(page, 'institute-row = ', len(lines))
        for line in lines:
            txt_str = str(line.text)  # преобразуем line.text в строку
            s = txt_str.find("студентов", 1)
            txt_str = txt_str.replace("\42", "")
            txt_str = txt_str[:s-2].strip()
            # print(txt_str)
            if txt_str in vuz_list:
                index = vuz_list.index(txt_str)
                if pattern_fo == '/заочное-обучение': za_fo_list[index] = "Есть"
                elif pattern_fo == '/очно-заочное-обучение': oz_fo_list[index] = "Есть"
            else:
                vuz_list.append(txt_str)
                budjet_mest_list.append(0)
                dogovor_mest_list.append(0)
                budjet_ball_list.append(0)
                dogovor_ball_list.append(0)
                cost_list.append(0)
                o4_fo_list.append("Нет")
                di_fo_list.append("Нет")
                if pattern_fo == '/заочное-обучение':
                    za_fo_list.append("Есть")
                    oz_fo_list.append("Нет")
                elif pattern_fo == '/очно-заочное-обучение':
                    za_fo_list.append("Нет")
                    oz_fo_list.append("Есть")

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

URL = 'https://vuzoteka.ru/вузы/Прикладная-информатика-09-03-03'
for page in range(33): # Выгрузим 33 страниц
    params = {'per_page':'10', 'page':page}
    response = requests.get(URL, params=params)
    # print(response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    lines = soup.find_all('div', class_='institute-row')
    # print(page, 'institute-row = ', len(lines))
    for line in lines:
        txt_str = str(line.text)  # преобразуем line.text в строку

        s = txt_str.find("студентов", 1)
        txt_str = txt_str.replace("\42", "")
        vuz_list.append(txt_str[:s-2].strip())

        budjet_mest, dogovor_mest = budjet_dogovor(pattern1)
        budjet_mest_list.append(budjet_mest)
        dogovor_mest_list.append(dogovor_mest)

        budjet_ball, dogovor_ball = budjet_dogovor(pattern3)
        budjet_ball_list.append(budjet_ball)
        dogovor_ball_list.append(dogovor_ball)

        thd, rur = budjet_dogovor(pattern4)
        cost_list.append(int(thd)*1000+int(rur))

o4_fo_list = ["Есть" for i in range(len(vuz_list))] # список очная форма обучения
za_fo_list = ["Нет" for i in range(len(vuz_list))] # список заочная форма обучения
oz_fo_list = ["Нет" for i in range(len(vuz_list))] # список очно-заочная форма обучения
di_fo_list = ["Нет" for i in range(len(vuz_list))] # список дистанциаонная форма обучения

# проверяем заочные отделения вузов
additional_proverka('/заочное-обучение')

# проверяем очно-заочные отделения вузов
additional_proverka('/очно-заочное-обучение')

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
df['Сайт'] = 'vuzoteka.ru'
# print(df)
df.to_csv('df_2.csv') # создаем csv





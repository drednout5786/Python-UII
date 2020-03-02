# LIGHT:
# Используя HH API, рассчитать среднюю зарплату в Москве по запросу "Python"
import requests

url_currency = 'https://www.cbr-xml-daily.ru/daily_json.js'
response_currency = requests.get(url_currency)
# print(response_currency.status_code)
result_json_currency = response_currency.json()
koef_USD = result_json_currency['Valute']['USD']['Value']
koef_EUR = result_json_currency['Valute']['EUR']['Value']
print(f"Курс валюты на сегодняшнюю дату: {result_json_currency['Date']}")
print(f"Курс доллара USD = {koef_USD}")
print(f"Курс Евро        = {koef_EUR}")

data_whole = []
wage = 0
sum_n = 0
url = 'https://api.hh.ru/vacancies'
for page in range(100): # Выгрузим 100 страниц вакансий
    params = {'text': 'Python', 'area':'1','per_page':'10', 'page':page}
    result = requests.get(url, params=params)
    result_json = result.json()
    data_whole.append(result_json)

for item in data_whole: # Перебираем вакансии в выгрузке
    data = item['items']
    n = 0 # Счетчик количество рассмотренных вакансий с указанными зарплатами
    sum_zp = 0 # Сумматор зарплат
    for record in data: # Перебираем вакансии
        if record['salary'] != None: # Есть ли инфа по зарпоате в вакансии
            salary = record['salary']
            if salary['from'] != None: # Есть ли инфа по минимальной зарпоате в вакансии
                n += 1
                # Учитываем курс валюты на сегодняшнюю дату
                if salary['currency'] == 'USD':
                    koef = koef_USD
                elif salary['currency'] == 'EUR':
                    koef = koef_EUR
                else: koef = 1
                # Учитываем как указана зарплата или диапазон зарплат
                if salary['to'] != None:  # Есть ли инфа по максимальной зарпоате в вакансии
                    sum_zp += koef*(salary['from'] + salary['to'])/2
                else:
                    sum_zp += koef*salary['from']
    wage += sum_zp
    sum_n += n
print(f"Средняя зарплата по Москве по ключевому слову {params['text']} составляет {round(wage/sum_n,2)} рублей.")


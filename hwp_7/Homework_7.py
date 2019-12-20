import datetime
import csv
import json
#import time
from docxtpl import DocxTemplate

def get_context(brand, model_a, volume, price_a): # возвращает словарь аргументов
    return {
        'brand': brand,
        'model_a': model_a,
        'volume': int(volume),
        'price_a': float(price_a),
    }

def from_template(brand, model_a, volume, price_a, template): # Вставка данных в шаблон.
    template = DocxTemplate(template) #Вордовский документ-Шаблон должен быть оформлен в шаблонизаторе Jinja.
    context = get_context(brand, model_a, volume, price_a)  # Словарь с содержанием вставки.
    template.render(context) # Передаем данные в шаблон - Рендерим.
    template.save(brand + '_' + str(datetime.datetime.now().date()) + '_report.docx') #Сохранение получившегося отчета.

def generate_report(brand, model_a, volume, price_a):
    template = 'report_avto.docx'
    document = from_template(brand, model_a, volume, price_a, template)

date_time = datetime.datetime.now()

# 3) Автоматически сгенерировать отчет о машине в формате doc.
begin_time = datetime.datetime.now()
start_time = begin_time

with open('avto_txt.txt') as f:
    line = f.readline() # считывание одной строки
dat = line.rstrip().split (sep=",")
brand = dat[0]
model_a = dat[1]
volume = dat[2]
price_a = dat[3]

generate_report(brand, model_a, volume, price_a)
finish_time = datetime.datetime.now()
delta = finish_time - start_time
print("Время генерации отчета в word %d микросекунд." % delta.microseconds)

# 4) Создать csv файл с данными о машине.
start_time = datetime.datetime.now()
car_data = [['brand', 'model_a', 'volume', 'price_a'],[brand, model_a, volume, price_a]]
with open('avto_csv.csv', 'w') as f:
    writer = csv.writer(f, delimiter = ';')
    writer.writerows(car_data)
    finish_time = datetime.datetime.now()
    delta = finish_time - start_time
    time_report = ["Report generation time (microseconds)", delta.microseconds]
    writer.writerows([time_report])
print('Запись в файл csv данных о машине завершена. Время генерации отчета', delta.microseconds, "microseconds.")

# 5) Создать json файл с данными о машине.
start_time = datetime.datetime.now()
dict_ex = get_context(brand, model_a, volume, price_a)
with open('avto_json.txt', 'w') as f:
    json.dump(dict_ex, f)
    finish_time = datetime.datetime.now()
    delta = finish_time - start_time
    time_report = {"Report generation time (microseconds): ": delta.microseconds}
    json.dump(time_report, f)
print('Запись в файл json данных о машине завершена. Время генерации отчета', delta.microseconds, "microseconds.")

finish_time = datetime.datetime.now()
delta = finish_time - begin_time
print("Время работы программы %d секунд." % delta.microseconds)


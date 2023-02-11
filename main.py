import re
import csv
from pprint import pprint

# читаем адресную книгу в формате CSV в список contacts_list

with open('phonebook_raw.csv', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=',')
    contacts_list = list(rows)

print('Данные загружены из файла phonebook_raw.csv')
print('-'*10)
print(f'Первоначальный набор данных:')
pprint(contacts_list)
print('-'*10)

#lastname,firstname,surname,organization,position,phone,email
contacts_dict = [['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']]
#обработка данных по Ф,И,О
persons = []
for pers in contacts_list:
  if pers[0] != 'lastname':
    fio = pers[0] + pers[1] + pers[2]
    pattern = r'[А-ЯЁ][а-яё]+'
    rez = re.findall(pattern, fio)
    if len(rez) < 3:
      n = 3 - len(rez)
      for _ in range(n):
        rez.append(' ')    
    #Обработка данных по телефонам
    phone = pers[5]
    #Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999;
    if phone.find('доб') != -1:
      pattern = r'(\+7|8)*\s*\(*([\d+]{3})\)*[-\s]*([\d+]{3})[-\s]*([\d+]{2})[-\s]*([\d+]{2})[-\s]*\(*[доб.]*\s*([\d]{4})*\)*'
      subst = r'+7(\2)\3-\4-\5 доб.\6'
      phone_number = re.sub(pattern, subst, phone)
    else: #если нет доб номера формат +7(999)999-99-99.
      pattern = r'(\+7|8)*\s*\(*([\d+]{3})\)*[-\s]*([\d+]{3})[-\s]*([\d+]{2})[-\s]*([\d+]{2})'
      subst = r'+7(\2)\3-\4-\5'
      phone_number = re.sub(pattern, subst, phone)
    
    #lastname,firstname,surname,organization,position,phone,email
    contacts_dict.append([rez[0], rez[1], rez[2], pers[3], pers[4], phone_number, pers[6]])

#удаление пробельных символов из пустых полей контакта
#для повышения качества хранимых данных и во избежание дальнейших проблем при запросах и обработке данных
for contact in contacts_dict:
  for n in range(2, len(contact)):
    if contact[n] == ' ':
      contact[n] = ''
    
#-------Объединение данных из дублирующихся записей--------
"""Исходя из имеющихся данных, условно предположим, что фамилия и имя в совокупности, могут быть взяты, 
в качестве уникального идентификатора (т.е. записи с одинаковыми Фамилией и Именем, но разным Отчеством в БД нет, 
хотя при использовании в реальных условиях, следует обязательно дополнить данный код проверкой на заполнение 
всех трех полей и в случае несоответствия отфильтровывать, либо дополнять такие записи недостающими данными)"""
n_dublicates = []
for n in range(0,len(contacts_dict)-1):
  contact1 = contacts_dict[n]
  for n_test in range(n+1,len(contacts_dict)):
    contact2 = contacts_dict[n_test]
    if contact1[0] == contact2[0] and contact1[1] == contact2[1]:
      n_dublicates.append(n_test)
      for m in range(2, len(contact1)):
        if contact1[m] == '' and contact2[m] != '':
          contact1[m] = contact2[m]
        else: 
          if contact2[m] != '' and contact1[m] != contact2[m]:
            print('Ошибка! Конфликт данных', 'contact1[m]', contact1[m], 'contact2[m]', contact2[m])

print('-'*10)
print('В наборе данных имеются дублирующиеся записи: ', n_dublicates)  
#удаление дубликатов
k = 0
for n_contact in n_dublicates:
  n_contact = n_contact - k
  contacts_dict.pop(n_contact)
  print(f'Дублирующая запись №{n_contact} удалена')
  k +=1
print('-'*10)
print(f'Результирующий набор данных:')
pprint(contacts_dict)

# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding='utf-8') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(contacts_dict)
print('-'*10)
print('Данные сохранены в файл phonebook.csv')
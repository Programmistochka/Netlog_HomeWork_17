import re
import csv
from pprint import pprint

# читаем адресную книгу в формате CSV в список contacts_list

with open('phonebook_raw.csv', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=',')
    contacts_list = list(rows)
#pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
# 1. Поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно. 
# В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О;
contact = {'lastname' : '', 
           'firstname' : '',
           'surname': '',
           'organization': '',
           'pozition': '',
           'phone': '',
           'email': ''}

contacts = []
for person in contacts_list:
    #if len(person[0])
    #contact = (' ').join(person[0])
    print('person[0]: ', person[0])
    print('person[1]: ', person[1])
    print('person[2]: ', person[2])
    fio = []
    count_spaces_fam = person[0].find(' ')
    print('count_spaces_fam = ', count_spaces_fam)
    lastname, firstname, surname = '', '', ''
    if count_spaces_fam == -1: #Фам, ...
        lastname = person[0]
        print('count_spaces_fam == -1')
        print('lastname = person[0] :', lastname)
        count_spaces_name = person[1].find(' ')
        if count_spaces_name == -1: #Фам, Имя, Отчество
            firstname = person[1]
            print('firstname = person[1]:', firstname)
            surname = person[2]
            print('surname = person[2]:', surname)
        else: ##Фам, Имя Отчество
            firstname = re.findall('^[А-ЯЁ][а-яё]+', person[1])
            firstname = firstname[0]
            print('firstname = re.findall("^[А-ЯЁ][а-яё]+", person[1]):', firstname)
            surname = re.findall('[А-ЯЁ][а-яё]+$', person[1])
            print('surname = re.findall("[А-ЯЁ][а-яё]+$", person[1]):', surname)
            surname = surname[0]
    else: #Фам Имя, Отч или Фам Имя Отч
        print('ELSE count_spaces_fam <>-1')
        lastname = re.findall('^[А-ЯЁ][а-яё]+', person[0])
        lastname = lastname[0]
        print('lastname = re.findall("^[А-ЯЁ][а-яё]+", person[0]): ', lastname)
        count_spaces_name = person[0][(count_spaces_fam+1):].find(' ')
        print('count_space_name = ', count_spaces_name)
        if count_spaces_name == -1: #Фам Имя, Отчество
            print('count_space_name == -1')
            firstname = re.findall('[А-ЯЁ][а-яё]+$', person[0][(count_spaces_fam+1):])
            firstname = firstname[0]
            print('firstname = re.findall("[А-ЯЁ][а-яё]+$", person[0]): ', firstname)
            surname = person[1]
            print('surname = person[1]: ', surname)
        else: #Фам Имя Отч
            print('count_space_name <> -1')
            firstname = re.findall("^[А-ЯЁ][а-яё]+", person[0][(count_spaces_fam+1):])
            firstname = firstname[0]
            print('firstname = re.findall("^[А-ЯЁ][а-яё]+", person[0][(count_spaces_fam+1):]):', firstname)
            surname = re.findall('[А-ЯЁ][а-яё]+$', person[0])
            surname = surname[0]
            print('surname = re.findall("[А-ЯЁ][а-яё]+$", person[0]):', surname)
    print('____Rez_____')
    print('lastname: ', lastname)
    print('firstname: ', firstname)
    print('surname: ', surname)
    print('--------------------------')  

# for person in contacts_list:
#     print('person', person)
#     #определить сколько слов в первом значении
#     spaces = re.findall(r'\s', str(person[0]))
#     print('spaces: ', spaces)
#     lastname = re.findall('^[А-ЯЁ][а-яё]+', person[0])
#     if not spaces:  #Фам
#         firstname = re.findall('\b[А-ЯЁ][а-яё]+',person[1])
#     else: #Фам+Имя
#         firstname = re.findall('\b[А-ЯЁ][а-яё]+',person[0])
#     print(lastname, firstname)
#     contact['lastname'] = lastname
#     contact['firstname'] = firstname
#     print('------')
#     contacts.append(contact)
# print('contacts:', contacts)

# # TODO 2: сохраните получившиеся данные в другой файл
# # код для записи файла в формате CSV
# with open("phonebook.csv", "w") as f:
#   datawriter = csv.writer(f, delimiter=',')
#   # Вместо contacts_list подставьте свой список
#   datawriter.writerows(contacts_list)

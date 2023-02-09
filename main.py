import re
import csv
from pprint import pprint

# читаем адресную книгу в формате CSV в список contacts_list

with open('phonebook_raw.csv', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=',')
    contacts_list = list(rows)
#pprint(contacts_list)

#lastname,firstname,surname,organization,position,phone,email
contacts_dict = []

persons = []
for pers in contacts_list:
  if pers[0] != 'lastname':
    #print(pers)
    fio = pers[0] + pers[1] + pers[2]
    #print(fio)
    pattern = r'[А-ЯЁ][а-яё]+'
    rez = re.findall(pattern, fio)
    if len(rez) == 3:
      #print('rez:', rez)
      whole_fio =(' ').join(rez)
       #Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999;
      phone = pers[5]
      print(whole_fio)
      print('phone: ', phone)
      if phone.find('доб') != -1:
        pattern = r'(\+7|8)*\s*\(*([\d+]{3})\)*[-\s]*([\d+]{3})[-\s]*([\d+]{2})[-\s]*([\d+]{2})[-\s]*\(*[доб.]*\s*([\d]{4})*\)*'
        subst = r'+7(\2)\3-\4-\5 доб.\6'
        phone_number = re.sub(pattern, subst, phone)
        print('new_phone: ', phone_number)
      else: #если нет доб номера формат +7(999)999-99-99.
        print('else')
        pattern = r'(\+7|8)*\s*\(*([\d+]{3})\)*[-\s]*([\d+]{3})[-\s]*([\d+]{2})[-\s]*([\d+]{2})'
        subst = r'+7(\2)\3-\4-\5'
        phone_number = re.sub(pattern, subst, phone)
        print('new_phone: ', phone_number)
      if whole_fio not in persons:
        persons.append(whole_fio)
        #lastname,firstname,surname,organization,position,phone,email
        contacts_dict.append([rez[0], rez[1], rez[2], pers[3], pers[4], phone_number, pers[6]])
    else:
      print(f'Внимание!  Не достаточно данных! {(" ").join(rez)}')
  #rezult = re.sub(pattern, 'o', fio)
pprint(contacts_dict)
print('---------------')
titles = [['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']]
contacts_dict = titles + contacts_dict
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding='utf-8') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(contacts_dict)
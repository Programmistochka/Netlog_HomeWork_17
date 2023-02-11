import re
import csv
from pprint import pprint

# читаем адресную книгу в формате CSV в список contacts_list

with open('phonebook_raw.csv', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=',')
    contacts_list = list(rows)

print(contacts_list)

#lastname,firstname,surname,organization,position,phone,email
contacts_dict = [['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']]

persons = []
for pers in contacts_list:
  if pers[0] != 'lastname':
    print(pers)
    fio = pers[0] + pers[1] + pers[2]
    #print(fio)
    pattern = r'[А-ЯЁ][а-яё]+'
    rez = re.findall(pattern, fio)
    if len(rez) < 3:
      n = 3 - len(rez)
      for _ in range(n):
        rez.append(' ')
      print(rez)    
    
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
    #if whole_fio not in persons:
    persons.append(whole_fio)
    
#lastname,firstname,surname,organization,position,phone,email
    print(rez[0], rez[1], rez[2], pers[3], pers[4], phone_number, pers[6])
    contacts_dict.append([rez[0], rez[1], rez[2], pers[3], pers[4], phone_number, pers[6]])
    #else:
    #  print(f'Внимание!  Не достаточно данных! {(" ").join(rez)}')
  #rezult = re.sub(pattern, 'o', fio)
pprint(contacts_dict)
print('---------------')

#удаление пробельных символов из пустых полей контакта, для повышения качества хранимых данных и во избежание дальнейших проблем при запросах и обработке данных
for contact in contacts_dict:
  for n in range(2, len(contact)):
    if contact[n] == ' ':
      contact[n] = ''
    
#-------Объединить данные из дублирующихся записей--------
#Исходя из имеющихся данных, условно предположим, что фамилия и имя в совокупности, могут быть взяты, в качестве уникального идентификатора (т.е. записи с одинаковыми Фамилией и Именем, но разным Отчеством в БД нет, хотя при использовании в реальных условиях, следует обязательно дополнить данный код проверкой на заполнение всех трех поле и в случае несоответствия отфильтровывать, либо дополнять такие записи недостающими данными)
print('')
print('___________find dublicats________________')



#print('contacts_dict')
#pprint(contacts_dict)
#print('-Количество контактов-', len(contacts_dict))
n_dublicates = []
for n in range(0,len(contacts_dict)-1):
  print('step', n)
  contact1 = contacts_dict[n]
  print('test: ', contact1)
  #pprint(contacts_for_test)
  #contacts_for_test.pop(n)
  #for contact2 in contacts_dict[n+1:]:
  for n_test in range(n+1,len(contacts_dict)):
    contact2 = contacts_dict[n_test]
    print('contact2: ', contact2)
    print('Поиск совпадения имен: ', contact1[0], '=', contact2[0], contact1[1], '=', contact2[1])
    if contact1[0] == contact2[0] and contact1[1] == contact2[1]:
      n_dublicates.append(n_test)
      print('---')
      print('СОВПАДЕНИЕ имен найдено: ', contact1[0], '=', contact2[0], contact1[1], '=', contact2[1])
      print(len(contact1))
      for m in range(2, len(contact1)):
        print('m', m)
        print('Сравнение для замены', contact1[m], contact2[m])
        if contact1[m] == '' and contact2[m] != '':
          print('ОТСУТСТВУЮЩИЕ данные найдены: ', contact1[m], contact2[m])
          contact1[m] = contact2[m]
          print('Инф по контакту дополнена')
        else: 
          if contact2[m] != '' and contact1[m] != contact2[m]:
            print('Ошибка! Конфликт данных', 'contact1[m]', contact1[m], 'contact2[m]', contact2[m])
      print('---')
  print('contact2_test_end\n') 

print('n_dublicates: ', n_dublicates)  
#удаление дубликатов
k = 0
for n_contact in n_dublicates:
  n_contact = n_contact - k
  contacts_dict.pop(n_contact)
  print(f'Дублирующая запись №{n_contact} удалена')
  k +=1




titles = [['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']]
contact_dict = titles + contacts_dict

print('contacts_dict\n', contacts_dict)
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding='utf-8') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(contacts_dict)
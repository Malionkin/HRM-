# Лабораторная работа №2 
## Справочники в PostGRES
Я придумал два справочника - справочник департаментов айти-компании, и справочник сотрудников этой компании:
![Image alt](https://github.com/Malionkin/HRM-/raw/master/src_hrm/Screenshot_1.png)
ERD-диаграмма вашему вниманию:
![Image alt](https://github.com/Malionkin/HRM-/raw/master/src_hrm/Screenshot_2.png)
Создал соответствующую базу данных в постгрес, вот таким образом можно вставлять значения в таблицы
![Image alt](https://github.com/Malionkin/HRM-/raw/master/src_hrm/Screenshot_3.png)
![Image alt](https://github.com/Malionkin/HRM-/raw/master/src_hrm/Screenshot_4.png)
Это были первые два шага лабы, теперь опишу третий; Создал приложение с помощью PyQT5, приложение подключается к моей базе данных и подтягивает из неё все доступные таблички:
![Image alt](https://github.com/Malionkin/HRM-/raw/master/src_hrm/Screenshot_5.png)
Нажимаем на кнопку Show Table, приложение показывает аналог Select * from table:
![Image alt](https://github.com/Malionkin/HRM-/raw/master/src_hrm/Screenshot_6.png)
Кстати вот так можно выбрать, какую именно табличку показать:
![Image alt](https://github.com/Malionkin/HRM-/raw/master/src_hrm/Screenshot_7.png)
Нажав кнопку Edit открывается возможность изменить значения:
![Image alt](https://github.com/Malionkin/HRM-/raw/master/src_hrm/Screenshot_8.png)
В данном случае меняю бюджет с 500 на 1000 и нажимаю кнопку Apply Changes и внесенные изменения уходят в базу данных ПРИ УСЛОВИИ ИХ КОРРЕКТНОСТИ!
![Image alt](https://github.com/Malionkin/HRM-/raw/master/src_hrm/Screenshot_9.png)
![Image alt](https://github.com/Malionkin/HRM-/raw/master/src_hrm/Screenshot_10.png)
![Image alt](https://github.com/Malionkin/HRM-/raw/master/src_hrm/Screenshot_11.png)
Также можно добавить строку, вылазит диалоговое окошко с параметрами таблицы, в которую хотим вставить:
![Image alt](https://github.com/Malionkin/HRM-/raw/master/src_hrm/Screenshot_12.png)
И кстати когда выбираем дату, вылазит такой календарик:
![Image alt](https://github.com/Malionkin/HRM-/raw/master/src_hrm/Screenshot_13.png)
Вот я добавил строчку
![Image alt](https://github.com/Malionkin/HRM-/raw/master/src_hrm/Screenshot_14.png)
И кстати есть возможность сортировки, смотрим:
![Image alt](https://github.com/Malionkin/HRM-/raw/master/src_hrm/Screenshot_15.png)
А если хочется, можно удалить строку:
![Image alt](https://github.com/Malionkin/HRM-/raw/master/src_hrm/Screenshot_16.png)
И эта строка также пропадет из базы:
![Image alt](https://github.com/Malionkin/HRM-/raw/master/src_hrm/Screenshot_17.png)
И вот такой момент: в таблице работников есть foreign key, айдишники названий департамента, в таблице они в виде айдишников, но если кто-то хочет добавить строку, то для простоты предоставлен интерфейс в виде выбора имени департамента, а в базу улетает автоматически айдишник:
![Image alt](https://github.com/Malionkin/HRM-/raw/master/src_hrm/Screenshot_18.png)
![Image alt](https://github.com/Malionkin/HRM-/raw/master/src_hrm/Screenshot_19.png)
Вот так:)

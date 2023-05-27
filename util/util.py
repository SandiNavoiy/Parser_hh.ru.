"""Скрипт для заполнения данными таблиц в БД Postgres."""
import json
from configparser import ConfigParser

import psycopg2

from scr.hh import HeadHunterAPI
from scr.DBManager import DBManage


def welcome():
    """Функция вывода приветствия"""
    print("                  Доброго времени суток")
    print("Вас приветствует программа по поиску, отбору вакансий \n"
          "и добавление их в базу данных PostgreSQL  с сайта: hh.ru\n")
    print("Далее будет представлено меню с возможными действиями")
    print("В случае первого использования программы или удаления файлов hh.json \n"
          "необходимо загрузить данные из сайта!")
    input("Нажмите любую клавишу для продолжения..................")



def interact_with_user():
    """Функция для взаимодействия с пользователем."""
    # Инициируем обьекты классов для работы
    hh_api = HeadHunterAPI()
    params = config()
    name_db = 'hh'
    try:
        db_manager = DBManage(name_db, params)
    except psycopg2.OperationalError:
        print("Ошибка подключенния к базе данных")
    else:



        while True:
            # Запускаем бесконечный цикл для работы меню
            print("Выберите действие:")
            print("1 - Загрузить свежую информацию с hh.ru")
            print("2 - Создание базы данных ")
            print("3 - Заполняем таблицы данными")
            print("4 - Вывод всех вакансий")
            print("5 - Вывод средней залплаты")
            print("6 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям")
            print("7 - Вывод списка всех вакансий, в названии которых содержатся ключевое слово")
            print("8 - Выйти")
            choice = input("Введите значение---")


            # Непосредствено работы меню выбора
            if choice == "1":
                # Загружаем информацию с hh
                key_words = input("Введите ключевое слово поисков:   ")
                hh_api.get_vacancies(key_words)
                # Сразу формируем список вакансий для работы,
                # чтобы не прописывать в дальнейшем в каждом варианте


            elif choice == "2":
                # создаем базу данных и таблицы
                db_manager.create_database()
                db_manager.create_tables()
                print(f"База данных {name_db} и таблицы employers и vacancies созданы")


            elif choice == "3":
                # Заполняем таблицы данными
                try:
                    data = json_reader()
                except FileNotFoundError:
                    print("Нет файла, загрузите вакансии с сайта")
                else:
                    for item in data['items']:
                        employer = item['employer']
                        employer_name = employer['name']
                        employer_description = employer['description']
                        employer_website = employer['alternate_url']
                        employer_id = db_manager.insert_employer(employer_name, employer_description, employer_website)
                        vacancy = item['name']
                        vacancy_salary = item['salary']
                        vacancy_link = item['alternate_url']
                        db_manager.insert_vacancy(employer_id, vacancy, vacancy_salary, vacancy_link)


            elif choice == "4":
                # Вывод вакансий в упрошенном виде с сортировкой
                db_manager.get_all_vacancies()


            elif choice == "5":
                # Средняя залплата по вакансиям
                db_manager.get_avg_salary


            elif choice == "6":
                #список всех вакансий, у которых зарплата выше средней по всем вакансиям
                db_manager.get_vacancies_with_higher_salary()


            elif choice == "7":
                # Вывод списка всех вакансий, в названии которых содержатся ключевое слово
                keyword =  input("Введите ключевое слово")
                db_manager.get_vacancies_with_keyword(keyword)


            elif choice == "8":
                # Выход
                db_manager.close_connection()
                print("--------------")
                print("Спасибо за обращение\n"
                      "До новых встреч!")
                print("--------------")
                break


            else:
                print("Введите правильное значение действий!!!!")




def config(filename="database.ini", section="postgresql"):
    """Словарь с данными для подключения к БД """
    # создаем парсер
    parser = ConfigParser()
    # читаем конфиг файл
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db

def json_reader():
    """    Читает данные из json файла"""
    with open("hh.json", 'r') as file:
        data = json.load(file)
    return data





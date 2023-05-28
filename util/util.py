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
        # Проверка подключения и наличие БД
        print("Ошибка подключенния к базе данных")
        print(f"Пытаемся создать БД с названием {name_db}")
        try:
            create_database(params)
            print("Перезапустите программу")
        except psycopg2.OperationalError:
            print("Проверьте фаерволл")

    else:

        while True:
            # Запускаем бесконечный цикл для работы меню
            print("Выберите действие:")
            print("1 - Загрузить свежую информацию с hh.ru")
            print("2 - Перевоздание базы данных и таблиц ")
            print("3 - Заполняем таблицы БД данными")
            print("4 - Вывод всех вакансий")
            print("5 - Вывод средней залплаты")
            print("6 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям")
            print("7 - Вывод списка всех вакансий, в названии которых содержатся ключевое слово")
            print("8 - Cписок всех компаний и количество вакансий у каждой компании")
            print("9 - Выйти")
            choice = input("Введите значение---")

            # Непосредствено работы меню выбора
            if choice == "1":
                # Загружаем информацию с hh
                #key_words = input("Введите ключевое слово поисков:   ")
                hh_api.get_employers()
                # Сразу формируем список вакансий для работы,
                # чтобы не прописывать в дальнейшем в каждом варианте

            elif choice == "2":
                # создаем базу данных и таблицы
                db_manager.create_database()
                db_manager.create_tables()
                print(f"База данных {name_db} и таблицы employers и vacancies созданы")

            elif choice == "3":
                # Заполняем БД данными
                try:
                    data = json_reader()
                except FileNotFoundError:
                    print("Нет файла, загрузите вакансии с сайта")
                else:
                    try:
                        db_manager.error_table()
                    except psycopg2.errors.UndefinedTable:
                        # Проверка наличие таблицы
                        print("Нет таблиц, создайте - пункт 2")
                    else:
                        try:

                            for item in data["items"]:
                                employer_id = item["id"]
                                employer_name = item["name"]
                                employer_description_vacancy = item["vacancies_url"]
                                employer_website = item["alternate_url"]
                                # Грузим в БД в таблицу employer
                                db_manager.insert_employer(employer_id, employer_name, employer_description_vacancy,
                                                           employer_website)
                                vacancy = item["name"]
                                vacancy_id = item['id']
                                try:
                                    # Заполняем и проверяем случай если з/п не указана
                                    vacancy_salary = int(item["salary"]["from"])
                                except TypeError:
                                    vacancy_salary = 0
                                vacancy_link = item["alternate_url"]
                                # Грузим в БД в таблицу vacancy
                                db_manager.insert_vacancy(vacancy_id, employer_id, vacancy, vacancy_salary,
                                                          vacancy_link)
                        except psycopg2.errors.UniqueViolation:
                            print("Данные уже занесены, повторно не требуется, или удалите и заново создайте таблицу и БД")
                        else:
                            print("Таблицы успешно заполнены")

            elif choice == "4":
                # Вывод всех вакансий
                try:
                    db_manager.error_table()
                except psycopg2.errors.UndefinedTable:
                    # Проверка наличие таблицы
                    print("Нет таблиц, создайте - пункт 2")
                else:
                    all_vacancies = db_manager.get_all_vacancies()
                    # Отрабатываем случай если в таблице нет данных
                    if all_vacancies == []:
                        print("Нет таблиц, создайте - пункт 2")
                    else:
                        for company, title, salary, link in all_vacancies:
                            print(f"Company: {company}")
                            print(f"Title: {title}")
                            print(f"Salary: {salary}")
                            print(f"Link: {link}")
                            print()

            elif choice == "5":
                # Средняя залплата по вакансиям
                try:
                    db_manager.error_table()
                except psycopg2.errors.UndefinedTable:
                    # Проверка наличие таблицы
                    print("Нет таблиц, создайте - пункт 2")
                else:
                    avg_salary = db_manager.get_avg_salary()
                    # Отрабатываем случай если в таблице нет данных
                    if avg_salary == None:
                        print("Не загружены данные в таблицы")
                    else:
                        print("Средняя зарплата(без учета нулевых значений по вакансиям:", avg_salary)

            elif choice == "6":
                # список всех вакансий, у которых зарплата выше средней по всем вакансиям
                try:
                    db_manager.error_table()
                except psycopg2.errors.UndefinedTable:
                    # Проверка наличие таблицы
                    print("Нет таблиц, создайте - пункт 2")
                else:
                    vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
                    # Отрабатываем случай если в таблице нет данных
                    if vacancies_with_higher_salary == []:
                        print("Нет таблиц, создайте - пункт 2")
                    else:
                        for company, title, salary, link in vacancies_with_higher_salary:
                            print(f"Работодатель: {company}")
                            print(f"Описание: {title}")
                            print(f"Зарплата: {salary}")
                            print(f"Ссылка: {link}")
                            print()

            elif choice == "7":
                # Вывод списка всех вакансий, в названии которых содержатся ключевое слово
                try:
                    db_manager.error_table()
                except psycopg2.errors.UndefinedTable:
                    # Проверка наличие таблицы
                    print("Нет таблиц, создайте - пункт 2")
                else:
                    keyword = input("Введите ключевое слово")
                    vacancies_with_keyword = db_manager.get_vacancies_with_keyword(keyword)
                    # Отрабатываем случай если в таблице нет данных
                    if vacancies_with_keyword == []:
                        print("Нет таблиц, создайте - пункт 2 или нет соответсвий")
                    else:
                        for company, title, salary, link in vacancies_with_keyword:
                            print(f"Работодатель: {company}")
                            print(f"Описание: {title}")
                            print(f"Зарплата: {salary}")
                            print(f"Ссылка: {link}")
                            print()

            elif choice == "8":
                # список всех компаний и количество вакансий у каждой компании
                try:
                    db_manager.error_table()
                except psycopg2.errors.UndefinedTable:
                    # Проверка наличие таблицы
                    print("Нет таблиц, создайте - пункт 2")
                else:
                    companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
                    # Отрабатываем случай если в таблице нет данных
                    if companies_and_vacancies_count == []:
                        print("Нет таблиц, создайте - пункт 2")
                    else:
                        print("Компания и количество вакансий:")
                        for company, count in companies_and_vacancies_count:
                            print(f"{company}: {count}")

            elif choice == "9":
                # Выход
                db_manager.close_connection()
                print("--------------")
                print("Спасибо за обращение\n"
                      "До новых встреч!")
                print("--------------")
                break

            elif choice == "11":
                # Выход
                c = json_reader()
                h = 0
                for i in c["items"]:
                    h = h +1
                    print(i)
                print(h)

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
    with open("hh.json", 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data


def create_database(params: dict):
    """Для первичного создания БД"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE hh")
    cur.close()
    conn.close()

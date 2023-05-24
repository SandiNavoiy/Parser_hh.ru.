"""Скрипт для заполнения данными таблиц в БД Postgres."""
from configparser import ConfigParser

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
    db_manager = DBManage('name_db', params)



    while True:
        # Запускаем бесконечный цикл для работы меню
        print("Выберите действие:")
        print("1 - Загрузить свежую информацию с hh.ru")
        print("2 - Создание базы данных ")
        print(" - Вывод вакансий в упрошенном виде с сортировкой")
        print(" - Добавление вакансии в избранное")
        print(" - Удаление вакансии из избранного")
        print("10 - Выйти")
        choice = input("Введите значение---")


        # Непосредствено работы меню выбора
        if choice == "1":
            # Загружаем информацию с hh
            key_words = input("Введите ключевое слово поисков:   ")
            hh_api.get_vacancies(key_words)
            # Сразу формируем список вакансий для работы,
            # чтобы не прописывать в дальнейшем в каждом варианте


        elif choice == "2":
            # создаеем базу данных и таблицы
            db_manager.create_database()
            db_manager.create_tables()
            print(f"База данных {name_db} и таблицы employers и vacancies созданны")




        elif choice == "3":
            # Вывод файла с избранным
            pass

        elif choice == "4":
            # Вывод вакансий в упрошенном виде с сортировкой
            pass

        elif choice == "5":
            # Добавление вакансии в избранное
            pass

        elif choice == "6":
            # Удаление вакансии из избранного
            pass

        elif choice == "7":
            # Очистка файла избранного (полная)
            pass

        elif choice == "8":
            # Вывод ТОП вакансий сортировкой
            # Валидация числа ввода
            pass

        elif choice == "9":
            # Вывод избранного в формате txt
            pass


        elif choice == "10":
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







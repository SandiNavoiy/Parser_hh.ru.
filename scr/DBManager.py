import psycopg2


class DBManage:
    """Класс для работы с данными в БД"""

    def __init__(self):
        self.conn = psycopg2.connect(dbname="head_hanter", user="postgres", password="1", host="localhost")
        self.cur = self.conn.cursor()


    def create_tables(self):
        """Создание таблиц для работодателей и вакансий"""
        self.cur.execute("CREATE TABLE employers (id SERIAL PRIMARY KEY, name VARCHAR(255), description TEXT, website VARCHAR(255))")


    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        pass

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием
          названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        pass

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        pass

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        pass

    def get_vacancies_with_keyword(self):
        """Получает список всех вакансий, в названии которых содержатся переданные
        в метод слова, например “python”"""
        pass

    def close_connection(self):
        """Закрытие соединения с базой данных"""
        self.cur.close()
        self.conn.close()

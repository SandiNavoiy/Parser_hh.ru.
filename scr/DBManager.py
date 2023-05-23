import psycopg2


class DBManage:
    """Класс для работы с данными в БД"""

    def __init__(self, database_name: str, params: dict):
        self.database_name = database_name
        self.params = params

    def create_database(self):
        """Создание базы данных """
        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE  IF EXISTS {self.database_name}")
        cur.execute(f"CREATE DATABASE {self.database_name}")
        conn.close()

    def create_tables(self):
        """Создание таблиц для работодателей и вакансий"""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("CREATE TABLE employers (id SERIAL PRIMARY KEY, name VARCHAR(255), description TEXT, "
                    "website VARCHAR(255))")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS vacancies (id SERIAL PRIMARY KEY, "
            "employer_id INTEGER, title VARCHAR(255), salary VARCHAR(50), link VARCHAR(255), "
            "FOREIGN KEY (employer_id) REFERENCES employers (id))")
        conn.close()

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

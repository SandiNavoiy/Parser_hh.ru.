import psycopg2


class DBManage:
    """Класс для работы с данными в БД"""

    def __init__(self, database_name: str, params: dict):
        self.database_name = database_name
        self.params = params
        self.conn = psycopg2.connect(dbname=self.database_name, **self.params)
        self.cur = self.conn.cursor()

    def connect_to_database(self):
        """Переподключение к базе данных"""
        self.conn.close()
        self.conn = psycopg2.connect(dbname=self.database_name, **self.params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def create_database(self):
        """Создание базы данных """
        self.conn = psycopg2.connect(dbname='postgres', **self.params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        # cur = conn.cursor()
        self.cur.execute(f"DROP DATABASE  IF EXISTS {self.database_name}")
        self.cur.execute(f"CREATE DATABASE {self.database_name}")
        self.conn.close()
        # conn.close()
        self.connect_to_database()

    def create_tables(self):
        """Создание таблиц для работодателей и вакансий"""
        self.connect_to_database()
        # conn = psycopg2.connect(dbname=self.database_name, **self.params)
        self.conn.autocommit = True
        # cur = conn.cursor()
        self.cur.execute("CREATE TABLE employers "
                         "(id SERIAL PRIMARY KEY, "
                         "name VARCHAR(255), "
                         "description TEXT, "
                         "website VARCHAR(255))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS vacancies "
                         "(id SERIAL PRIMARY KEY, "
                         "employer_id INTEGER,"
                         "title VARCHAR(255), "
                         "salary VARCHAR(50), "
                         "link VARCHAR(255), "
                         "FOREIGN KEY (employer_id) REFERENCES employers (id))")
        # conn.close()

    def insert_employer(self, name, description, website):
        """"Вставка данных о работодателе в таблицу employers"""
        self.connect_to_database()
        # conn = psycopg2.connect(dbname=self.database_name, **self.params)
        self.conn.autocommit = True
        # cur = conn.cursor()
        self.cur.execute(
            """
            INSERT INTO employers (name, description, website)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (name, description, website)
        )
        employer_id = self.cur.fetchone()[0]
        # conn.close()
        return employer_id

    def insert_vacancy(self, employer_id, title, salary, link):
        """Вставка данных о вакансии в таблицу vacancies"""
        # conn = psycopg2.connect(dbname=self.database_name, **self.params)
        self.connect_to_database()
        self.conn.autocommit = True
        # cur = conn.cursor()
        self.cur.execute(
            """
            INSERT INTO vacancies (employer_id, title, salary, link)
            VALUES (%s, %s, %s, %s)
            """,
            (employer_id, title, salary, link)
        )
        # conn.close()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        # conn = psycopg2.connect(dbname=self.database_name, **self.params)
        self.connect_to_database()
        self.conn.autocommit = True
        # cur = conn.cursor()
        self.cur.execute(
            """
            SELECT employers.name, COUNT(vacancies.id)
            FROM employers
            LEFT JOIN vacancies ON employers.id = vacancies.employer_id
            GROUP BY employers.name
            """
        )
        result = self.cur.fetchall()
        # conn.close()
        return result

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием
          названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        # conn = psycopg2.connect(dbname=self.database_name, **self.params)
        self.connect_to_database()
        self.conn.autocommit = True
        # cur = conn.cursor()
        self.cur.execute(
            """
            SELECT employers.name, vacancies.title, vacancies.salary, vacancies.link
            FROM vacancies
            INNER JOIN employers ON vacancies.employer_id = employers.id
            """
        )
        result = self.cur.fetchall()
        # conn.close()
        return result

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        # conn = psycopg2.connect(dbname=self.database_name, **self.params)
        self.connect_to_database()
        self.conn.autocommit = True
        # cur = conn.cursor()
        self.cur.execute(
            """
            SELECT AVG(CAST(REPLACE(salary, 'руб.', '') AS INTEGER))
            FROM vacancies
            """
        )
        result = self.cur.fetchone()[0]
        # conn.close()
        return result

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        self.connect_to_database()
        avg_salary = self.get_avg_salary()
        # conn = psycopg2.connect(dbname=self.database_name, **self.params)
        self.conn.autocommit = True
        # cur = conn.cursor()
        self.cur.execute(
            """
            SELECT employers.name, vacancies.title, vacancies.salary, vacancies.link
            FROM vacancies
            INNER JOIN employers ON vacancies.employer_id = employers.id
            WHERE CAST(REPLACE(vacancies.salary, 'руб.', '') AS INTEGER) > %s
            """,
            (avg_salary,)
        )
        result = self.cur.fetchall()
        # conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные
        в метод слова"""
        self.connect_to_database()
        #conn = psycopg2.connect(dbname=self.database_name, **self.params)
        self.conn.autocommit = True
        #cur = conn.cursor()
        self.cur.execute(
            """
            SELECT employers.name, vacancies.title, vacancies.salary, vacancies.link
            FROM vacancies
            INNER JOIN employers ON vacancies.employer_id = employers.id
            WHERE vacancies.title ILIKE %s
            """,
            ('%' + keyword + '%',)
        )
        result = self.cur.fetchall()
        #conn.close()
        return result

    def close_connection(self):
        """Закрытие соединения с базой данных"""
        self.connect_to_database()
        # self.cur.close()
        # self.conn.close()

import psycopg2


class DBManage:
    """Класс для работы с данными в БД"""

    def __init__(self, database_name: str, params: dict):
        self.database_name = database_name
        self.params = params
        self.conn = psycopg2.connect(dbname=self.database_name, **self.params)
        self.cur = self.conn.cursor()

    def connect_to_database(self):
        """Переподключение к базе данных, чтоб не писать одно и тоже"""
        self.conn.close()
        self.conn = psycopg2.connect(dbname=self.database_name, **self.params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def create_database(self):
        """Создание базы данных или удаление текущей"""
        self.conn.close()  # Закрыть текущее соединение
        # Создать новое соединение для выполнения операций создания и удаления базы данных
        conn_temp = psycopg2.connect(dbname='postgres', **self.params)
        conn_temp.autocommit = True
        cur_temp = conn_temp.cursor()
        # Удалить базу данных, если она существует
        cur_temp.execute(f"DROP DATABASE IF EXISTS {self.database_name}")
        # Создать базу данных
        cur_temp.execute(f"CREATE DATABASE {self.database_name}")
        # Закрыть временное соединение
        cur_temp.close()
        conn_temp.close()
        # Подключиться заново к базе данных
        self.connect_to_database()

    def create_tables(self):
        """Создание таблиц для работодателей и вакансий"""
        self.connect_to_database()
        # Запрос SQL
        self.cur.execute("CREATE TABLE IF NOT EXISTS employers "
                         "(employer_id INTEGER PRIMARY KEY, "
                         "name VARCHAR(255), "
                         "employer_city TEXT, "
                         "website VARCHAR(255))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS vacancies "
                         "(vacancy_id varchar(10) PRIMARY KEY, "
                         "employer_id INTEGER,"
                         "title VARCHAR(255), "
                         "salary INTEGER, "
                         "link VARCHAR(255), "
                         "FOREIGN KEY (employer_id) REFERENCES employers (employer_id))"
                         )

    def insert_employer(self, employer_id, name, description, website):
        """"Вставка данных о работодателе в таблицу employers"""
        self.connect_to_database()
        # Запрос SQL

        self.cur.execute(
            """
            INSERT INTO employers (employer_id, name, employer_city, website)
            VALUES (%s, %s, %s, %s)
            
            """,
            (employer_id, name, description, website)
        )



    def insert_vacancy(self, vacancy_id, employer_id, title, salary, link):
        """Вставка данных о вакансии в таблицу vacancies"""
        self.connect_to_database()
        # Запрос SQL
        self.cur.execute(
            """
            INSERT INTO vacancies (vacancy_id, employer_id, title, salary, link)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (vacancy_id, employer_id, title, salary, link)
        )

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        self.connect_to_database()
        # Запрос SQL
        self.cur.execute(
            """
            SELECT employers.name, COUNT(vacancy_id)
            FROM employers
            LEFT JOIN vacancies USING(employer_id)
            GROUP BY employers.name
            """
        )
        result = self.cur.fetchall()
        return result

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием
          названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        self.connect_to_database()
        # Запрос SQL
        self.cur.execute(
            """
            SELECT employers.name, vacancies.title, vacancies.salary, vacancies.link
            FROM vacancies
            INNER JOIN employers USING(employer_id)
            """
        )
        result = self.cur.fetchall()
        return result

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        self.connect_to_database()
        # Запрос SQL
        self.cur.execute(
            """
            SELECT ROUND(AVG(salary)) 
            FROM vacancies
            WHERE salary <> 0;
            """
        )
        result = self.cur.fetchone()[0]
        return result

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        self.connect_to_database()
        avg_salary = self.get_avg_salary()
        # Запрос SQL
        self.cur.execute(
            """
            SELECT employers.name, vacancies.title, vacancies.salary, vacancies.link
            FROM vacancies
            INNER JOIN employers USING(employer_id)
            WHERE vacancies.salary > %s
            """,
            (avg_salary,)
        )
        result = self.cur.fetchall()
        return result

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные
        в метод слова"""
        self.connect_to_database()
        # Запрос SQL
        self.cur.execute(
            """
            SELECT employers.name, vacancies.title, vacancies.salary, vacancies.link
            FROM vacancies
            INNER JOIN employers USING(employer_id)
            WHERE vacancies.title ILIKE %s
            """,
            ('%' + keyword + '%',)
        )
        result = self.cur.fetchall()
        return result

    def error_table(self):
        """Отлов ошибки отсудствия таблиц, чтоб не ломать код"""
        self.connect_to_database()
        # Запрос SQL
        self.cur.execute(
            """
            SELECT * 
            FROM vacancies
          
            """
        )

    def close_connection(self):
        """Закрытие соединения с базой данных"""
        self.connect_to_database()
        self.cur.close()
        self.conn.close()

import requests
import psycopg2


class DBManager:
    def __init__(self, db_name, user, password, host, port):
        self.conn = psycopg2.connect(
            database=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cur = self.conn.cursor()

    def create_tables(self):
        # Создание таблиц для работодателей и вакансий
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS employers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                description TEXT,
                website VARCHAR(255)
            )
            """
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                employer_id INTEGER,
                title VARCHAR(255),
                salary VARCHAR(50),
                link VARCHAR(255),
                FOREIGN KEY (employer_id) REFERENCES employers (id)
            )
            """
        )
        self.conn.commit()

    def insert_employer(self, name, description, website):
        # Вставка данных о работодателе в таблицу employers
        self.cur.execute(
            """
            INSERT INTO employers (name, description, website)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (name, description, website)
        )
        employer_id = self.cur.fetchone()[0]
        self.conn.commit()
        return employer_id

    def insert_vacancy(self, employer_id, title, salary, link):
        # Вставка данных о вакансии в таблицу vacancies
        self.cur.execute(
            """
            INSERT INTO vacancies (employer_id, title, salary, link)
            VALUES (%s, %s, %s, %s)
            """,
            (employer_id, title, salary, link)
        )
        self.conn.commit()

    def get_companies_and_vacancies_count(self):
        # Получение списка компаний и количества вакансий
        self.cur.execute(
            """
            SELECT employers.name, COUNT(vacancies.id)
            FROM employers
            LEFT JOIN vacancies ON employers.id = vacancies.employer_id
            GROUP BY employers.name
            """
        )
        result = self.cur.fetchall()
        return result

    def get_all_vacancies(self):
        # Получение списка всех вакансий с указанием компании, названия, зарплаты и ссылки
        self.cur.execute(
            """
            SELECT employers.name, vacancies.title, vacancies.salary, vacancies.link
            FROM vacancies
            INNER JOIN employers ON vacancies.employer_id = employers.id
            """
        )
        result = self.cur.fetchall()
        return result

    def get_avg_salary(self):
        # Получение средней зарплаты по вакансиям
        self.cur.execute(
            """
            SELECT AVG(CAST(REPLACE(salary, 'руб.', '') AS INTEGER))
            FROM vacancies
            """
        )
        result = self.cur.fetchone()[0]
        return result

    def get_vacancies_with_higher_salary(self):
        # Получение списка вакансий с зарплатой выше средней
        avg_salary = self.get_avg_salary()
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
        return result

    def get_vacancies_with_keyword(self, keyword):
        # Получение списка вакансий, в названии которых содержится заданное ключевое слово
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
        return result

    def close_connection(self):
        # Закрытие соединения с базой данных
        self.cur.close()
        self.conn.close()


def get_hh_data():
    # Получение данных о компаниях и вакансиях с сайта hh.ru
    api_url = 'https://api.hh.ru/vacancies'
    params = {
        'text': 'python',
        'area': '1',  # Москва
        'per_page': '100'
    }
    response = requests.get(api_url, params=params)
    data = response.json()
    return data


def process_hh_data(data):
    # Обработка данных о компаниях и вакансиях с сайта hh.ru
    db_manager = DBManager('your_db_name', 'your_username', 'your_password', 'your_host', 'your_port')
    db_manager.create_tables()

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

    db_manager.close_connection()


if __name__ == '__main__':
    hh_data = get_hh_data()
    process_hh_data(hh_data)
    db_manager = DBManager('your_db_name', 'your_username', 'your_password', 'your_host', 'your_port')
    companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
    all_vacancies = db_manager.get_all_vacancies()
    avg_salary = db_manager.get_avg_salary()
    vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
    vacancies_with_keyword = db_manager.get_vacancies_with_keyword('python')
    db_manager.close_connection()

    print("Companies and Vacancies Count:")
    for company, count in companies_and_vacancies_count:
        print(f"{company}: {count}")

    print("\nAll Vacancies:")
    for company, title, salary, link in all_vacancies:
        print(f"Company: {company}")
        print(f"Title: {title}")
        print(f"Salary: {salary}")
        print(f"Link: {link}")
        print()

    print("Average Salary:", avg_salary)

    print("\nVacancies with Higher Salary:")
    for company, title, salary, link in vacancies_with_higher_salary:
        print(f"Company: {company}")
        print(f"Title: {title}")
        print(f"Salary: {salary}")
        print(f"Link: {link}")
        print()

    print("\nVacancies with Keyword 'python':")
    for company, title, salary, link in vacancies_with_keyword:
        print(f"Company: {company}")
        print(f"Title: {title}")
        print(f"Salary: {salary}")
        print(f"Link: {link}")
        print()




def employees(file_mame):
    """"""
    with open(os.path.join(file_mame), 'r') as f:
        reader = csv.reader(f)
        next(reader)
        conn = psycopg2.connect(dbname="north", user="postgres", password="1", host="localhost")
        cur = conn.cursor()
        id_emp = 1
        for row in reader:
            cur.execute("INSERT INTO employees (id_emp, first_name, last_name, title, birth_date, notes) VALUES (%s, %s, %s, %s, %s, %s)",
                        (id_emp, row[0], row[1], row[2], row[3], row[4]))
            id_emp += 1

    conn.commit()
    cur.close()
    conn.close()



customers("north_data/customers_data.csv")
employees("north_data/employees_data.csv")
orders("north_data/orders_data.csv")
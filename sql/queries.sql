---def create_database(params: dict):
CREATE DATABASE hh

---def create_tables(self):
---Создание таблиц для работодателей и вакансий
CREATE TABLE IF NOT EXISTS employers
                         (employer_id INTEGER PRIMARY KEY,
                         name VARCHAR(255),
                         employer_city TEXT,
                         website VARCHAR(255)))
CREATE TABLE IF NOT EXISTS vacancies
                         (vacancy_id varchar(10) PRIMARY KEY,
                         employer_id INTEGER,
                         title VARCHAR(255),
                         salary INTEGER,
                         link VARCHAR(255),
                         FOREIGN KEY (employer_id) REFERENCES employers (employer_id)))


---def insert_employer:
---Вставка данных о работодателе в таблицу employers"""
INSERT INTO employers (employer_id, name, employer_city, website)
VALUES (%s, %s, %s, %s)

---def insert_vacancy):
---Вставка данных о вакансии в таблицу vacancies"""
INSERT INTO vacancies (vacancy_id, employer_id, title, salary, link)
VALUES (%s, %s, %s, %s, %s)

---def get_companies_and_vacancies_count(self):
---Получает список всех компаний и количество вакансий у каждой компании
SELECT employers.name, COUNT(vacancy_id)
FROM employers
LEFT JOIN vacancies USING(employer_id)
GROUP BY employers.name

---def get_all_vacancies:
---Получает список всех вакансий с указанием
          названия компании, названия вакансии и зарплаты и ссылки на вакансию
SELECT employers.name, vacancies.title, vacancies.salary, vacancies.link
FROM vacancies
INNER JOIN employers USING(employer_id)


---def get_avg_salary(self):
---Получает среднюю зарплату по вакансиям
SELECT ROUND(AVG(salary))
FROM vacancies
WHERE salary <> 0;


---def get_vacancies_with_higher_salary:
---Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
SELECT employers.name, vacancies.title, vacancies.salary, vacancies.link
FROM vacancies
INNER JOIN employers USING(employer_id)
WHERE vacancies.salary > %s


---def get_vacancies_with_keyword(self, keyword):
---Получает список всех вакансий, в названии которых содержатся переданные
SELECT employers.name, vacancies.title, vacancies.salary, vacancies.link
FROM vacancies
INNER JOIN employers USING(employer_id)
WHERE vacancies.title ILIKE %s


---def error_table(self):
---Отлов ошибки отсудствия таблиц, чтоб не ломать код
SELECT * FROM vacancies

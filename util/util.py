"""Скрипт для заполнения данными таблиц в БД Postgres."""
import csv
import os
import psycopg2

def customers(file_mame):
    """"""
    with open(os.path.join(file_mame), 'r') as f:
        reader = csv.reader(f)
        next(reader)
        conn = psycopg2.connect(dbname="north", user="postgres", password="1", host="localhost")
        cur = conn.cursor()
        for row in reader:
            cur.execute("INSERT INTO customers (customer_id, company_name, contact_name) VALUES (%s, %s, %s)",
                        (row[0], row[1], row[2]))

    conn.commit()
    cur.close()
    conn.close()

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

def orders(file_mame):
    """"""
    with open(os.path.join(file_mame), 'r') as f:
        reader = csv.reader(f)
        next(reader)
        conn = psycopg2.connect(dbname="north", user="postgres", password="1", host="localhost")
        cur = conn.cursor()
        for row in reader:
            cur.execute("INSERT INTO orders (order_id, customer_id, employee_id, order_date, ship_city) VALUES (%s, %s, %s, %s, %s)",
                        (row[0], row[1], row[2], row[3], row[4]))

    conn.commit()
    cur.close()
    conn.close()

customers("north_data/customers_data.csv")
employees("north_data/employees_data.csv")
orders("north_data/orders_data.csv")
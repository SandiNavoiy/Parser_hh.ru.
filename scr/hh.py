import json

import requests

from scr.abc import Employer


class HeadHunterAPI(Employer):
    """Класс для работы с сайтом HeadHunter"""

    def __init__(self):
        """Инициация класса, атрибутом URL"""
        self.__url = 'https://api.hh.ru/employers/'


    def get_employers(self):
        """Метод работы и получения данных от API hh о работадателях"""

        params = {

            'area': 1,
            'per_page': 100,  # Кол-во вакансий на 1 странице
            'only_with_vacancies': 'true'
        }
        try:
            self.req = requests.get(self.__url, params).json()
        except requests.exceptions.RequestException as e:
            print(f"Нет соединения, ошибка{e}. СМЕНИ РЕГИОН VPN!! ")
        else:
            print("Информация с hh.ru успешно загружена")
            with open("hh.json", "w", encoding="utf-8") as f:
                json.dump(self.req, f, indent=2, ensure_ascii=False)

    def __repr__(self):
        """Метод вывода полученой информации"""
        return self.req
    def get_vacancies(self,url_vac):
        """Метод работы и получения данных от API hh о работадателях"""
        vacancies_data = {'items': []}
        params = {

            'area': 1,
            'per_page': 100,  # Кол-во вакансий на 1 странице
            'only_with_vacancies': 'true'
        }
        try:
            response = requests.get(url_vac, params).json()
        except requests.exceptions.RequestException as e:
            print(f"Нет соединения, ошибка{e}. СМЕНИ РЕГИОН VPN!! ")
        else:
            #data = response.json()
            #vacancies_data['items'].extend(data['items'])
            return response

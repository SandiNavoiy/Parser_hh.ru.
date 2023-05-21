# Абстрактные классы
from abc import ABC, abstractmethod


class Employer(ABC):
    """Абстрактный класс для работы с API сайтов"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class VacancyStorage(ABC):
    """Абстрактный класс для классов работы с данными вакансий"""

    @abstractmethod
    def sorting(self, vacancy):
        pass

    @abstractmethod
    def list_of_vacancy(self):
        pass

    @abstractmethod
    def get_vacancies(self, **kwargs):
        pass

    @abstractmethod
    def top(self, vacancy):
        pass


class JsonSave(ABC):
    """ Абстрактный класс работы с файлами json"""

    @abstractmethod
    def add_vacancy(self):
        pass

    @abstractmethod
    def remove_vacancy(self):
        pass

    @abstractmethod
    def clean_file_favourites(self):
        pass

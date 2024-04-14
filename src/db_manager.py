import psycopg2
from src.config import config


class DBManager:
    """Класс для управления базой данных."""

    def __init__(self, db_name):
        """Инициализация объекта DBManager."""
        self.db_name = db_name

    def execute_query(self, query) -> list:
        """Выполнение SQL-запроса к базе данных."""
        conn = psycopg2.connect(dbname=self.db_name, **config())
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()
        return result

    def get_companies_and_vacancies_count(self):
        """Получение списка компаний и количества вакансий, которые они предоставляют."""
        result = self.execute_query('SELECT employers.name, COUNT(vacancies.employer_id) AS vacancies_count FROM employers LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id GROUP BY employers.name')
        return result

    def get_all_vacancies(self):
        """Получение всех вакансий из базы данных."""
        result = self.execute_query('SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.url FROM employers JOIN vacancies using (employer_id)')
        return result

    def get_avg_salary(self):
        """Получение средней зарплаты по всем вакансиям."""
        result = self.execute_query('SELECT AVG(salary_from) AS payment_avg FROM vacancies')
        return result

    def get_vacancies_with_higher_salary(self):
        """Получение вакансий с зарплатой выше средней."""
        result = self.execute_query('SELECT * FROM vacancies WHERE salary_from > (select AVG(salary_from) FROM vacancies)')
        return result

    def get_vacancies_with_keyword(self, keywords):
        """Получение вакансий, содержащих указанные ключевые слова."""
        result = self.execute_query(f'SELECT * FROM vacancies WHERE name LIKE \'%{keywords}%\'')
        return result

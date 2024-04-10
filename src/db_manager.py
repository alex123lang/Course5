import psycopg2


class DBManager:
    def __init__(self, db_name, user, password, host):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host

    @staticmethod
    def execute_query(query) -> list:
        conn = psycopg2.connect(dbname='db_name', user='user', password='password', host='host')
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()
        return result

    def get_companies_and_vacancies_count(self):
        result = self.execute_query('SELECT employers.name, COUNT(vacancies.employer_id) AS vacancies_count FROM employers LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id GROUP BY employers.name')
        return result

    def get_all_vacancies(self):
        result = self.execute_query('SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.url FROM employers JOIN vacancies using (employer_id)')
        return result

    def get_avg_salary(self):
        result = self.execute_query('SELECT AVG(salary_from) AS payment_avg FROM vacancies')
        return result

    def get_vacancies_with_higher_salary(self):
        result = self.execute_query('SELECT * FROM vacancies WHERE salary_from > (select AVG(salary_from) FROM vacancies)')
        return result

    def get_vacancies_with_keyword(self, keywords):
        result = self.execute_query(f'SELECT * FROM vacancies WHERE name LIKE \'%{keywords}%\'')
        return result

import requests


class HeadHunterAPI:
    """Класс для взаимодействия с API HeadHunter для получения информации о работодателях и вакансиях."""

    def __init__(self, companies):
        """Инициализирует HeadHunterAPI с переданным списком компаний."""

        self.url_employers = 'https://api.hh.ru/employers/'
        self.url_vacancies = 'https://api.hh.ru/vacancies?employer_id={}'
        self.companies = companies

    def get_employers(self):
        """Получает список работодателей на основе предоставленных названий компаний."""

        employers = []
        for company in self.companies:
            params = {'text': company}
            response = requests.get("http://api.hh.ru/employers/", params)
            if response.status_code == 200:
                data = sorted(response.json()["items"], key=lambda x: len(x['name']))
                for employer in data:
                    employers.append(
                        {"id": employer["id"], "name": employer["name"], "open_vacancies": employer["open_vacancies"]})
                    break
            else:
                raise Exception(f"Не удалось получить вакансии. Код статуса: {response.status_code}")
        return employers

    def get_vacancies_by_employer(self, employer_id):
        """Получает список вакансий для конкретного работодателя."""

        url_vacancies = self.url_vacancies.format(employer_id)
        response = requests.get(url_vacancies, params={'per_page': 100})
        if response.status_code == 200:
            return response.json()["items"]
        else:
            raise Exception(f"Не удалось получить вакансии. Код статуса: {response.status_code}")

    def get_vacancies(self):
        """Получает список вакансий для всех предоставленных компаний."""

        vacancies = []
        for i in self.get_employers():
            for vacancy in self.get_vacancies_by_employer(i["id"]):
                vacancies.append({
                    "id": vacancy["id"],
                    "name": vacancy["name"],
                    "salary_from": vacancy['salary']['from'] if vacancy['salary'] else 0,
                    "salary_to": vacancy['salary']['to'] if vacancy['salary'] else 0,
                    "url": vacancy["alternate_url"],
                    "employer": vacancy["employer"]["id"],
                })
        return vacancies

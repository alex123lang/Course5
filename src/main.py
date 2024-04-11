from src.db_manager import DBManager
from src.add_data import create_database, create_tables, insert_data_into_tables


def main():
    db_name = input('Название базы данных: ')
    list_employers = ['Ozon', 'Альфа-Банк', 'Яндекс', 'МТС', 'Ростелеком', 'Зенит', 'Аэрофлот', 'VK', 'X5 Group', 'Тинькофф']
    dbm = DBManager(db_name)
    create_database(db_name)
    create_tables(db_name)
    insert_data_into_tables(db_name, list_employers)

    while True:

        new = input(
            '1 - список всех компаний и кол-во вакансий у каждой компании\n'
            '2 - список всех вакансий с указанием названия компании, вакансии, зарплаты и ссылки на вакансию\n'
            '3 - средняя зарплата по вакансиям\n'
            '4 - список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
            '5 - список вакансий, в названии которых содержится ключевое слово\n'
            'Exit - закончить\n'
        )

        if new == '1':
            print(dbm.get_companies_and_vacancies_count())
        elif new == '2':
            print(dbm.get_all_vacancies())
        elif new == '3':
            print(dbm.get_avg_salary())
        elif new == '4':
            print(dbm.get_vacancies_with_higher_salary())
        elif new == '5':
            keyword = str(input('Найти: '))
            print(dbm.get_vacancies_with_keyword(keyword))
        elif new == 'Exit'.lower():
            break


if __name__ == "__main__":
    main()

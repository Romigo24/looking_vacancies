import requests
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable


def create_table(table, title):
    table_data = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ]
    ]

    for language, info in table.items():
        table_data.append([
            language,
            info['vacancies_found'],
            info['vacancies_processed'],
            info['average_salary']
        ])
    
    table = AsciiTable(table_data)
    table.title = title
    return table.table


def find_jobs_on_languages_hh():
    jobs_on_languages_hh = dict()
    programming_languages = [
        'Python',
        'Java',
        'JavaScript'
    ]

    for language in programming_languages:
        url = 'https://api.hh.ru/vacancies'
        vacancies_found = 0
        salaries = []
        page = 0
        moscow_area_id = 1
        days_period = 30
        vacancies_per_page = 100

        while True:
            payload = {
                'text': f'программист {language}',
                'area': moscow_area_id,
                'period': days_period,
                'per_page': vacancies_per_page,
                'page': page
            }
            response = requests.get(url, params=payload)
            response.raise_for_status()

            vacancies_from_page = response.json()
            vacancies_found = vacancies_from_page['found']

            for vacancy in vacancies_from_page['items']:
                salary_values = vacancy.get('salary')
                if salary_values and salary_values.get('currency') == 'RUR':
                    salary_from = salary_values.get('from')
                    salary_to = salary_values.get('to')
                    salary = predict_rub_salary(salary_from, salary_to)
                    if salary:
                        salaries.append(salary)

            if vacancies_from_page['pages'] == page + 1:
                break

            page += 1

        job_and_salary = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': len(salaries),
            'average_salary': int(sum(salaries) / len(salaries)) if salaries else 0
        }

        jobs_on_languages_hh[language] = job_and_salary

    return jobs_on_languages_hh


def find_jobs_on_languages_superjob(secret_key):
    jobs_on_languages_superjob = dict()
    programming_languages = [
        'Python',
        'Java',
        'JavaScript'
    ]
    
    for language in programming_languages:
        url= 'https://api.superjob.ru/2.0/vacancies/'
        page = 0
        moscow_town_id = 4
        it_vacancy_category = 48
        vacacies_per_page = 100
        vacancies_found = 0
        salaries = []

        while True:
            payload = {
                'town': moscow_town_id,
                'catalogues': it_vacancy_category,
                'keyword': {language},
                'count': vacacies_per_page,
                'page': page
            }
            headers = {
                'X-Api-App-Id': secret_key,
            }
            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()

            vacancies_response = response.json()
            vacancies_from_page = vacancies_response['objects']
            vacancies_found = vacancies_response['total']

            if not vacancies_from_page:
                break

            for vacancy in vacancies_from_page:
                salary_from = vacancy.get('payment_from')
                salary_to = vacancy.get('payment_to')
                if salary_from or salary_to:
                    salary = predict_rub_salary(salary_from, salary_to)
                    if salary:
                        salaries.append(salary)
            page += 1

        if salaries:
            average_salary = sum(salaries) / len(salaries)
        else:
            average_salary = 0

        jobs_on_languages_superjob[language] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': len(salaries),
            'average_salary': average_salary
        }
    return jobs_on_languages_superjob


def predict_rub_salary(salary_from, salary_to):
    if not salary_from and not salary_to:
        return None
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from and not salary_to:
        return salary_from * 1.2
    elif not salary_from and salary_to:
        return salary_to * 0.8
    

if __name__ == '__main__':
    load_dotenv()
    secret_key = os.environ['SUPERJOB_SECRET_KEY']
    
    hh_table = find_jobs_on_languages_hh()
    superjob_table = find_jobs_on_languages_superjob(secret_key)

    print(create_table(hh_table, 'HeadHunter Moscow'))
    print(create_table(superjob_table, 'SuperJob Moscow'))
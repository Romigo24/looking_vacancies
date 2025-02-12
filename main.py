import requests

def get_vacancies_count():
    url = 'https://api.hh.ru/vacancies'
    payload = {
        'text': 'программист',
        'area': 1,
        'date': 30
    }
    response = requests.get(url, params=payload)
    response.raise_for_status
    data = response.json()
    vacancies = data.get('items', [])
    moscow_vacancies = [vacancy for vacancy in vacancies if vacancy['area']['name'] == 'Москва']
    print(f"Количество вакансий в Москве за последний месяц: {len(moscow_vacancies)}")
    for vacancy in moscow_vacancies:
        print(vacancy['name'], vacancy['published_at'])

def job_on_languages():
    programming_languages = [
        'JavaScript',
        'Java',
        'Python',
        'Ruby',
        'PHP',
        'C++',
        'C#',
        'C',
        'Go',
        'Shell']
    languages_count = dict()
    url = 'https://api.hh.ru/vacancies'
    
    for language in programming_languages:
        payload = {
            'text': f'программист {language}',
            'area': '1',
            'period': '30'
        }
        response = requests.get(url, params=payload)
        response.raise_for_status()
        vacancies = response.json()['found']
        languages_count[language] = vacancies
    print(languages_count)

def predict_rub_salary(vacancy):
    url = 'https://api.hh.ru/vacancies'
    payload = {
        'text': vacancy,
        'area': '1',
        'period': '30',
        'per_page': 20
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    vacancies = response.json()['items']
    for salary in vacancies:
        salary = salary['salary']
        if salary is None:
            print(None)
        elif salary['currency'] != 'RUR':
            print(None)
        elif (salary['from'] is not None) and (salary['to'] is not None):
            print((salary['from']+salary['to'])/2)
        else:
            print(salary['from'])

if __name__ == '__main__':
    predict_rub_salary('программист Python')

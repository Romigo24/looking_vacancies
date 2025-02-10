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


if __name__ == '__main__':
    get_vacancies_count()

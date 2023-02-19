import requests
from dotenv import load_dotenv
import os
from pprint import pprint
from common import predict_salary, predict_average_salary


def get_vacancies(params, superjob_key):
    headers = {'X-Api-App-Id': superjob_key,
               'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=headers, params=params)
    response.raise_for_status()
    response = response.json()
    return response['total'], response['objects']


def process_page(params, superjob_key):
    total, vacancies = get_vacancies(params, superjob_key)
    salaries = []
    for vacancy in vacancies:
        payment_from = vacancy['payment_from']
        payment_to = vacancy['payment_to']
        predicted_salary = predict_salary(payment_from, payment_to)
        if predicted_salary:
            salaries.append(predicted_salary)
    return {'total': total, 'salaries': salaries}


def process_pages(params, superjob_key):
    processed_page = process_page(params, superjob_key)
    total = processed_page['total']
    salaries = processed_page['salaries']
    page = 1
    per_page = 20
    if total % per_page:
        pages = int(total / per_page) + 1
    else:
        pages = total / per_page
    while page <= pages:
        params['page'] = page
        salaries += process_page(params, superjob_key)['salaries']
        page += 1
    vacancies_processed, average_salary = predict_average_salary(salaries)
    lang_statistic = {
        'vacancies_found': total,
        'average_salary': average_salary,
        'vacancies_processed': vacancies_processed
    }
    return lang_statistic


def get_sj_vacancies_statistics(langs, params, superjob_key):
    lang_statistics = {}
    for lang in langs:
        params['keyword'] = f'программист {lang}'
        params['page'] = 0
        lang_statistics[lang] = process_pages(params, superjob_key)
    return lang_statistics


if __name__ == '__main__':
    load_dotenv()
    superjob_key = os.getenv('SUPER_JOB_KEY')
    langs = os.getenv('LANGS').split(', ')
    sj_params = {
        'town': os.getenv('SJ_AREA'),
        'period': os.getenv('SJ_PERIOD')
    }
    pprint(get_sj_vacancies_statistics(langs, sj_params, superjob_key))

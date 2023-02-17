import requests
from dotenv import load_dotenv
import os
from pprint import pprint
from common import predict_average_salary, predict_salary


def predict_rub_salary_for_superjob(vacancy):
    payment_from = vacancy['payment_from']
    payment_to = vacancy['payment_to']
    return predict_salary(payment_from, payment_to)


def get_vacancies(params, superjob_key):
    headers = {'X-Api-App-Id': superjob_key,
               'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=headers, params=params)
    response.raise_for_status()
    response = response.json()
    output = {
        'total': response['total'],
        'vacancies': response['objects']
    }
    return output


def process_page(params, superjob_key):
    vacancies = get_vacancies(params, superjob_key)
    total = vacancies['total']
    vacancies = vacancies['vacancies']
    salaries = []
    for vacancy in vacancies:
        predicted_salary = predict_rub_salary_for_superjob(vacancy)
        if predicted_salary:
            salaries.append(predicted_salary)
    processed_page = {
        'salaries': salaries,
        'total': total
    }
    return processed_page


def process_pages(params, superjob_key):
    processed_page = process_page(params, superjob_key)
    salaries = processed_page['salaries']
    lang_statistic = {'vacancies_found': processed_page['total']}
    page = 1
    per_page = 20
    if processed_page['total'] % per_page:
        pages = int(processed_page['total'] / per_page) + 1
    else:
        pages = processed_page['total'] / per_page
    while page <= pages:
        params['page'] = page
        salaries += process_page(params, superjob_key)['salaries']
        page += 1
    lang_statistic['average_salary'] = predict_average_salary(salaries)
    lang_statistic['vacancies_processed'] = len(salaries)
    return lang_statistic


def get_sj_vacancies_statistics(langs, params, superjob_key):
    lang_statistics = {}
    for lang in langs:
        params['keyword'] = f'программист {lang}'
        params['page'] = 0
        lang_statistics.update({lang: process_pages(params, superjob_key)})
    return lang_statistics


if __name__ == '__main__':
    load_dotenv()
    superjob_key = os.getenv('SUPER_JOB_KEY')
    langs = os.getenv('LANGS').split(', ')
    sj_params = {'town': os.getenv('SJ_AREA'),
                 'period': os.getenv('SJ_PERIOD')}
    pprint(get_sj_vacancies_statistics(langs, sj_params, superjob_key))

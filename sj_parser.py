import requests
from dotenv import load_dotenv
import config
import os
from pprint import pprint
from common import predict_average_salary


def predict_rub_salary_for_superjob(vacancy):
    payment_from = vacancy['payment_from']
    payment_to = vacancy['payment_to']
    if (not payment_from) and (not payment_to):
        return None
    elif not payment_from:
        return payment_to*0.8
    elif not payment_to:
        return payment_from*1.2
    else:
        return (payment_from + payment_to)/2


def get_vacancies(params):
    headers = {'X-Api-App-Id': os.getenv('SUPER_JOB_KEY'),
               'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=headers, params=params)
    response.raise_for_status()
    response = response.json()
    output = {
        'total': response['total'],
        'vacancies': response['objects']
    }
    return output


def process_page(params):
    vacancies = get_vacancies(params)
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


def process_pages(params):
    processed_page = process_page(params)
    salaries = processed_page['salaries']
    lang_statistic = {'vacancies_found': processed_page['total']}
    page = 1
    per_page = 20
    if processed_page['total'] % per_page == 0.0:
        pages = processed_page['total'] / per_page
    else:
        pages = int(processed_page['total'] / per_page) + 1
    while page <= pages:
        params['page'] = page
        salaries += process_page(params)['salaries']
        page += 1
    lang_statistic['average_salary'] = predict_average_salary(salaries)
    lang_statistic['vacancies_processed'] = len(salaries)
    return lang_statistic


def get_sj_vacancies_statistics(langs, params):
    lang_statistics = {}
    for lang in langs:
        params['keyword'] = f'программист {lang}'
        params['page'] = 0
        lang_statistics.update({lang: process_pages(params)})
    return lang_statistics


if __name__ == '__main__':
    load_dotenv()
    params = config.params_sj
    langs = config.langs
    pprint(get_sj_vacancies_statistics(langs, params))

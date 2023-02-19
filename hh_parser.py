import requests
import os
from dotenv import load_dotenv
from pprint import pprint
from common import predict_salary, predict_average_salary


def predict_rub_salary(vacancy):
    salary = vacancy['salary']
    if not salary:
        return None
    payment_from = salary['from']
    payment_to = salary['to']
    return predict_salary(payment_from, payment_to)


def process_page(params):
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    response.raise_for_status()
    response = response.json()
    page, pages = response['page'], response['pages']
    vacancies = response['items']
    salaries = []
    for vacancy in vacancies:
        predicted_salary = predict_rub_salary(vacancy)
        if predicted_salary:
            salaries.append(predicted_salary)
    processed_page = {
        'page': page,
        'pages': pages,
        'salaries': salaries,
        'total': response['found']
    }
    return processed_page


def process_pages(params):
    processed_page = process_page(params)
    pages = processed_page['pages']
    salaries = processed_page['salaries']
    page = 1
    while page <= pages:
        params['page'] = page
        salaries += process_page(params)['salaries']
        page += 1
    vacancies_processed, average_salary = predict_average_salary(salaries)
    lang_statistic = {
        'vacancies_found': processed_page['total'],
        'average_salary': average_salary,
        'vacancies_processed': vacancies_processed
    }
    return lang_statistic


def get_hh_vacancies_statistics(langs, params):
    lang_statistics = {}
    for lang in langs:
        params['text'] = f'программист {lang}'
        params['page'] = 0
        lang_statistics[lang] = process_pages(params)
    return lang_statistics


if __name__ == '__main__':
    load_dotenv()
    langs = os.getenv('LANGS').split(', ')
    hh_params = {
        'area': os.getenv('HH_AREA'),
        'period': os.getenv('HH_PERIOD')
    }
    pprint(get_hh_vacancies_statistics(langs, hh_params))

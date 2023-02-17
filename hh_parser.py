import requests
import config
from pprint import pprint
from dotenv import load_dotenv
from common import predict_average_salary


def predict_rub_salary(vacancy):
    salary_meta = vacancy['salary']
    if salary_meta:
        if salary_meta['from'] is None:
            return salary_meta['to']*0.8
        elif salary_meta['to'] is None:
            return salary_meta['from']*1.2
        else:
            return (salary_meta['from'] + salary_meta['to'])/2
    else:
        return None


def process_page(params):
    responce = requests.get('https://api.hh.ru/vacancies', params=params)
    responce.raise_for_status()
    responce = responce.json()
    page, pages = responce['page'], responce['pages']
    vacancies = responce['items']
    salaries = []
    for vacancy in vacancies:
        predicted_salary = predict_rub_salary(vacancy)
        if predicted_salary:
            salaries.append(predicted_salary)
    output = {
        'page': page,
        'pages': pages,
        'salaries': salaries,
        'total': responce['found']
    }
    return output


def process_pages(params):
    processed_page = process_page(params)
    pages = processed_page['pages']
    salaries = processed_page['salaries']
    lang_statistic = {'vacancies_found': processed_page['total']}
    page = 1
    while page <= pages:
        params.update({'page': page})
        salaries += process_page(params)['salaries']
        page += 1
    lang_statistic.update({'average_salary': predict_average_salary(salaries),
                           'vacancies_processed': len(salaries)})
    return lang_statistic


def get_hh_vacancies_statistics(langs, params):
    lang_statistics = {}
    for lang in langs:
        params.update({'text': f'программист {lang}',
                       'page': 0})
        lang_statistics.update({lang: process_pages(params)})
    return lang_statistics


if __name__ == '__main__':
    load_dotenv()
    params = config.params_hh
    langs = config.langs
    pprint(get_hh_vacancies_statistics(langs, params))

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
    output = {
        'page': page,
        'pages': pages,
        'salaries': salaries,
        'total': response['found']
    }
    return output


def process_pages(params):
    processed_page = process_page(params)
    pages = processed_page['pages']
    salaries = processed_page['salaries']
    lang_statistic = {'vacancies_found': processed_page['total']}
    page = 1
    while page <= pages:
        params['page'] = page
        salaries += process_page(params)['salaries']
        page += 1
    lang_statistic['average_salary'] = predict_average_salary(salaries)
    lang_statistic['vacancies_processed'] = len(salaries)
    return lang_statistic


def get_hh_vacancies_statistics(langs, params):
    lang_statistics = {}
    for lang in langs:
        params['text'] = f'программист {lang}'
        params['page'] = 0
        lang_statistics.update({lang: process_pages(params)})
    return lang_statistics


if __name__ == '__main__':
    load_dotenv()
    params = config.hh_params
    langs = config.langs
    pprint(get_hh_vacancies_statistics(langs, params))

import os
import terminaltables.ascii_table
from dotenv import load_dotenv
from hh_parser import get_hh_vacancies_statistics
from sj_parser import get_sj_vacancies_statistics


def convert_to_table_rows(statistics):
    table_rows = [[
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата'
    ]]
    for statistic in statistics:
        table_rows.append([statistic,
                           statistics[statistic]['vacancies_found'],
                           statistics[statistic]['vacancies_processed'],
                           statistics[statistic]['average_salary']])
    return table_rows


def print_table(title, table_rows):
    table = terminaltables.ascii_table.AsciiTable(table_rows)
    table.title = title
    print(table.table)


if __name__ == '__main__':
    load_dotenv()
    superjob_key = os.getenv('SUPER_JOB_KEY')
    langs = os.getenv('LANGS').split(', ')
    sj_params = {
        'town': os.getenv('SJ_AREA'),
        'period': os.getenv('SJ_PERIOD')
    }
    hh_params = {
        'area': os.getenv('HH_AREA'),
        'period': os.getenv('HH_PERIOD')
    }
    sj_statistics = get_sj_vacancies_statistics(langs, sj_params, superjob_key)
    hh_statistics = get_hh_vacancies_statistics(langs, hh_params)
    print_table('SuperJob Moscow', convert_to_table_rows(sj_statistics))
    print()
    print_table('HeadHunter Moscow', convert_to_table_rows(hh_statistics))

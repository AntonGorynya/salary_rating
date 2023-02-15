import terminaltables.ascii_table
import config
from dotenv import load_dotenv
from hh_parser import vacancies_statistics_hh
from sj_parser import vacancies_statistics_sj


def convert_to_table_data(statistics):
    table_data = []
    table_data.append([
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата'
    ])
    for statistic in statistics:
        table_data.append([statistic,
                           statistics[statistic]['vacancies_found'],
                           statistics[statistic]['vacancies_processed'],
                           statistics[statistic]['average_salary']])
    return table_data


def print_table(title, data):
    table_data = convert_to_table_data(data)
    table = terminaltables.ascii_table.AsciiTable(table_data)
    table.title = title
    print(table.table)


if __name__ == '__main__':
    load_dotenv()
    langs = config.langs
    params_sj = config.params_sj
    params_hh = config.params_hh
    sj_statistics = vacancies_statistics_sj(langs, params_sj)
    hh_statistics = vacancies_statistics_hh(langs, params_hh)
    print_table('SuperJob Moscow', sj_statistics)
    print()
    print_table('HeadHunter Moscow', hh_statistics)

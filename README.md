# Сбор статиски по средней заработной плате с сервисов HeadHunter SuperJob

Данный репозитарий представляет собой скрипт, который собирают статистику по средней заработной платене по языкам программирования с сервисов HeadHunter и SuperJob

### Как установить

Перед установкой создайте файл **.env** вида:
```
SUPER_JOB_KEY='<Токен>'
```
Токен для SuperJob вы можете получить на сайте https://api.superjob.ru/

Так же необходимо создать файл **config.py** в корне программы вида:
```
params_hh = {'area': 1,
             'period': 5}
params_sj = {'town': 'Москва',
             'period': 0}
langs = ['Python', '1C', 'Java', 'Javascript']
```
где:
в params_hh укажите id города. `1` для Москвы и интервал поиска. Укажите `None`  для поиска по всем вакансиям с сервиса HeadHunter.
в params_sj укажите название города. И интервал поиска. `0` для поиска по всем вакансиям по SuperJob.

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Пример запуска

Ниже представлен примеры запуска скриптов.

```
Salary_rating> python .\main.py 
+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Python                | 19               | 18                  | 81448.78         |
| 1C                    | 59               | 48                  | 156632.08        |
| Java                  | 5                | 3                   | 155000.0         |
| Javascript            | 30               | 29                  | 96261.31         |
+-----------------------+------------------+---------------------+------------------+

+HeadHunter Moscow------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Python                | 933              | 267                 | 177531.84        |
| 1C                    | 1646             | 889                 | 159805.42        |
| Java                  | 736              | 194                 | 206354.06        |
| Javascript            | 1126             | 507                 | 161727.02        |
+-----------------------+------------------+---------------------+------------------+

Process finished with exit code 0


```


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
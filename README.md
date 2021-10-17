# Habr Carrier parser
Простая тулза для сбора вакансий из RSS ленты хабр карьеры. Все аккуратно собирается в базу для последующего анализа. Выполнено в виде микросервиса с возможность развертывания на бесплатном уровне в heroku.Предусмотрено так же создание дампа данных для того чтоб можно было забрать в другое место.

### Для локальной разработки достаточно:
1. поставить пакеты из requirements-dev.txt  -- pip install -r requirements-dev.txt
2. авторизоваться в heroku-cli и выбрать проект
3. Настроить postgres, redis на heroku
4. Запустить ./run_from_local_migrations_on_heroku.bash чтоб прошли миграции для БД
5. запустить что вам требуется из баш скриптов run_local*

### Для развертывания на heroku:
1. Жмакнуть по кнопке
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
2. Подцепить сервис Postgres и redis
3. Засунуть в настройка переменных среды параметр ACCESS_MAGIC_KEY в котором указать случайные значения. Это пригодиться если захочется выгружать дампы.
4. Указать в переменных среды RSS_URL адрес откуда тянуть данные
https://career.habr.com/vacancies/rss?page=1&per_page=25&q=Ruby
5. Запустить ./run_from_local_migrations_on_heroku.bash чтоб прошли миграции для БД
6. Прописать в heroku cron : cd src/ && python3 parser_hc.py
7. Enjoy

### quality
[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-black.svg)](https://sonarcloud.io/dashboard?id=saintbyte_carrier-analyzer)

[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=saintbyte_carrier-analyzer&metric=bugs)](https://sonarcloud.io/dashboard?id=saintbyte_carrier-analyzer)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=saintbyte_carrier-analyzer&metric=code_smells)](https://sonarcloud.io/dashboard?id=saintbyte_carrier-analyzer)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=saintbyte_carrier-analyzer&metric=sqale_index)](https://sonarcloud.io/dashboard?id=saintbyte_carrier-analyzer)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=saintbyte_carrier-analyzer&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=saintbyte_carrier-analyzer)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=saintbyte_carrier-analyzer&metric=security_rating)](https://sonarcloud.io/dashboard?id=saintbyte_carrier-analyzer)

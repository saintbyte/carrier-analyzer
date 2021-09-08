# Habr Carrier parser
Простая тулза для сбора вакансий из RSS ленты хабр карьеры. Все аккуратно собирается в базу для последующего анализа. Выполнено в виде микросервиса с возможность развертывания на бесплатном уровне в heroku.Предусмотрено так же создание дампа данных для того чтоб можно было забрать в другое место. 

###Для локальной разработки достаточно:
1. поставить пакеты из requirements-dev.txt  -- pip install -r requirements-dev.txt
2. авторизоваться в heroku-cli и выбрать проект 
3. Настроить postgres, redis на heroku 
4. Запустить ./run_from_local_migrations_on_heroku.bash чтоб прошли миграции для БД
5. запустить что вам требуется из баш скриптов run_local* 

###Для развертывания на heroku:
1. Жмакнуть по кнопке
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
2. Запустить ./run_from_local_migrations_on_heroku.bash чтоб прошли миграции для БД
3. Прописать в heroku cron : python3 parser_hc.py
4. Enjoy

### quality
[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-black.svg)](https://sonarcloud.io/dashboard?id=saintbyte_carrier-analyzer)

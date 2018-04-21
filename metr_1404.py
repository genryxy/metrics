import json
import requests
import urllib.request
import datetime
import os
import sqlite3

date = datetime.date.today()

yesterday_f = open('yesterday.txt', 'r')
for line in yesterday_f:
    users_yes = line.strip().split()
yesterday_f.close()

today_f = open('/logs/'+str(date)+'.log', 'r')

cur = 1

successful_requests = 0  # успешные запросы (1)
users = []  # уникальные пользователи (2)
countries = set()  # страны по IP для вычисления количества стран (3)
super_users = set()  # пользователи, которые были сегодня, но не были вчера (4)
queries_dict = {}  # для количества посещений самой часто посещаемой страницы (5)
hours = [0 for i in range(0, 24)]  # Час (номер) когда было больше всего запросов к сайту (6)
hours_queries = -1  # Час (номер) когда было больше всего запросов к сайту (6)
hour_unique_users = set()  # уникальные посетители по часам (7)
max_unique_users = 0  # наибольшее число уникальных посетителей в час за день (7)
hour_max_unique = -1  # час (номер) когда было на сайте наибольшее число уникальных посетителей (7)
unique_queries = set()  # для количества уникальных пользователей по странам (8)
countries_unique_users_dict = {}  # для количества уникальных пользователей по странам (8)
countries_unique_users_str = ''
countries_queries_dict = {}  # для количества запросов по странам (9)
countries_queries_str = ''
average_numb_queries_dict = {}  # среднее количество запросов на одного пользователя по странам (10)
average_numb_queries_str = ''
site_from = set()  # множество сайтов, с которых переходили (11)
site_from_dict = {}  # множество сайтов, с которых переходили (11)
site_from_num = -1  # кол-во сайтов, с которых переходили (11)
english_translatings = 0  # количество переводов, при помощи подсчета количества вхождений 'en-US' (12)
cur = 0

for line in today_f:
    print(cur)
    cur += 1
    main_line = line.strip().split()
    if main_line[8] == '200':
        IP = main_line[0]
        hour = int(main_line[3][13:15])
        hours[hour] += 1
        successful_requests += 1  # кол-во запросов

        site = main_line[10][1:-1]
        if site not in site_from:
            site_from.add(site)
            site_from_dict[site] = 1
        else:
            site_from_dict[site] += 1  # сайты, с которых переходили

        try:
            coun1 = requests.get('http://api.sypexgeo.net/json/{}'.format(IP))
            coun = json.loads(coun1.text)
            country = coun['country']['name_en']
        except TypeError:
            country = '?'

        if country not in countries:
            countries.add(country)
            countries_queries_dict[country] = 1
        else:
            countries_queries_dict[country] += 1  # количество запросов по странам

        query = main_line[6]
        if query not in unique_queries:
            unique_queries.add(query)
            queries_dict[query] = 1
        else:
            try:
                queries_dict[query] += 1
            except KeyError:
                queries_dict[query] = 1
        visiting_most_visited_page = max(queries_dict.values())  # количество посещений самой часто посещаемой страницы

        if 'en-US' in line:
            english_translatings += 1  # кол-во переведенных страниц на английский

        if IP not in users_yes and IP in users:
            super_users.append(IP)

        if IP not in users:
            users.add(IP)
            countries_unique_users_dict[country] = 1
        else:
            countries_unique_users_dict[country] += 1  # Количество уникальных пользователей по странам

        if hours[hour] > 1:
            hour_unique_users.add(IP)
        else:
            if max_unique_users < len(hour_unique_users):
                max_unique_users = len(hour_unique_users)
                hour_max_unique = hour - 1  # Час, когда было на сайте наибольшее число уникальных посетителей
            hour_unique_users.clear()

hour_unique_users.clear()
today_f.close()

for i in range(len(hours)):
    if hours[i] > hours_queries:
        hours_queries = hours[i]
        max_hour = i

for i in site_from_dict.keys():
    if site_from_dict[i] > site_from_num:
        site_from_num = site_from_dict[i]

countries_unique_users_list = sorted(countries_unique_users_dict.items(), key=lambda item: item[0])
countries_queries_list = sorted(countries_queries_dict.items(), key=lambda item: item[0])
for i in range(len(countries_queries_dict)):
    average_numb_queries_dict[countries_queries_list[i][0]] = round((countries_queries_list[i][1] / countries_unique_users_list[i][1]), 2)

for i in countries_unique_users_list:
    countries_unique_users_str += str(i[0]) + '-' + str(i[1]) + '; '

for i in countries_queries_list:
    countries_queries_str += str(i[0]) + '-' + str(i[1]) + '; '

for i in average_numb_queries_dict.keys():
    average_numb_queries_str += i + '-' + str(average_numb_queries_dict[i]) + '; '

int_info = [(date, successful_requests, len(users), len(countries), len(super_users), visiting_most_visited_page,
             max_hour, hour_max_unique, site_from_num, english_translatings)]
countries_info = [(date, countries_unique_users_str, countries_queries_str, average_numb_queries_str)]

#yest_f = open('yesterday.txt', 'w')
#yest_f.write(' '.join(users))
#yest_f.close()

conn = sqlite3.connect('/home/AndreyKorokhov/Metries.db')
c = conn.cursor()

c.execute(
    "CREATE TABLE IF NOT EXISTS Metries_int (Date Date, Succesful_requests INTEGER, Unq_users INTEGER, Countries INTEGER, Today_users INTEGER, Visiting_most_visited_page INTEGER,  Top_requests_hour INTEGER, Top_unique_users_hour INTEGER, Unq_outgoing_sites INTEGER, Russian_translatings INTEGER);")
c.execute(
    "CREATE TABLE IF NOT EXISTS Metries_countries (Date Date, Unq_users_per_country text, Requests_per_country text, Average_num_of_requests_per_country text);")

c.executemany("INSERT INTO Metries_int VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", int_info)
c.executemany("INSERT INTO Metries_countries VALUES (?, ?, ?, ?)", countries_info)

conn.commit()
conn.close()
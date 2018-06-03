
# coding: utf-8

# In[ ]:


import json
import requests
import urllib.request
import datetime
import os
import sqlite3

date = str(datetime.date.today()-datetime.timedelta(days=1))  

yesterday_f = open('yesterday.txt', 'r')
for line in yesterday_f:
    users_yes = line.strip().split()
yesterday_f.close()

today_f = open('/logs/'+str(date)+'.log', 'r')

successful_requests = 0  # успешные запросы (1)
users = set()  # уникальные пользователи (2)
countries = set()  # страны по IP для вычисления количества стран (3)
super_users = set()  # пользователи, которые были сегодня, но не были вчера (4)
queries_dict = {}  # для количества посещений самой часто посещаемой страницы (5)
hours = [0 for i in range(0, 24)]  # Час (номер) когда было больше всего запросов к сайту (6)
hours_queries = -1  # Час (номер) когда было больше всего запросов к сайту (6)
hours_users = [0 for i in range(0, 24)]  # уникальные посетители по часам (7)
hour_max_unique_q = -1  # час (номер) когда было на сайте наибольшее число уникальных посетителей (7)
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
country_user = {}

for line in today_f:
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
            if IP in country_user.keys():
                country = country_user[IP]
            else:
                coun1 = requests.get('http://freegeoip.net/json/{}'.format(IP))
                coun = json.loads(coun1.text)
                country = coun['country_name']
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


        if IP not in users:
            users.add(IP)
            hours_users[hour] += 1
            if IP not in users_yes:
                super_users.add(IP)
            country_user[IP] = country 
            try:
                countries_unique_users_dict[country] += 1  # Количество уникальных пользователей по странам
            except Exception:
                countries_unique_users_dict[country] = 1

today_f.close()

for i in range(len(hours_users)):
    if hours_users[i] > hour_max_unique_q:
        hour_max_unique_q = hours_users[i]
        hour_max_unique = i

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
    average_numb_queries_dict[countries_queries_list[i][0]] = round((countries_queries_list[i][1] / countries_unique_users_list[i][1]), 3)

for i in countries_unique_users_list:
    countries_unique_users_str += str(i[0]) + '-' + str(i[1]) + '; '

for i in countries_queries_list:
    countries_queries_str += str(i[0]) + '-' + str(i[1]) + '; '


for i in average_numb_queries_dict.keys():
    average_numb_queries_str += i + '-' + str(average_numb_queries_dict[i]) + '; '

int_info = [(date, successful_requests, len(users), len(countries), len(super_users), visiting_most_visited_page,
             max_hour, hour_max_unique, site_from_num, english_translatings)]
countries_info = [(date, countries_unique_users_str, countries_queries_str, average_numb_queries_str)]

yest_f = open('yesterday.txt', 'w')
yest_f.write(' '.join(users))
yest_f.close()

conn = sqlite3.connect('/home/AndreyKorokhov/Metries.db')
c = conn.cursor()

c.execute(
    "CREATE TABLE IF NOT EXISTS Metries_int (Date Date, Successful_requests INTEGER, Unq_users INTEGER, Countries INTEGER, Today_users INTEGER, Visiting_most_visited_page INTEGER,  Top_requests_hour INTEGER, Top_unique_users_hour INTEGER, Unq_outgoing_sites INTEGER, English_translatings INTEGER);")
c.execute(
    "CREATE TABLE IF NOT EXISTS Metries_countries (Date Date, Unq_users_per_country text, Requests_per_country text, Average_num_of_requests_per_country text);")

c.executemany("INSERT INTO Metries_int VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", int_info)
c.executemany("INSERT INTO Metries_countries VALUES (?, ?, ?, ?)", countries_info)

conn.commit()
conn.close()


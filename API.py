import sys
sys.path.append('.localpip')
from flask import Flask, jsonify
import datetime
import sqlite3

app = Flask(__name__)

def make_query(*params):
    conn = sqlite3.connect('Metries.db')
    c = conn.cursor()
    c.execute(*params)
    retur = c.fetchall()
    conn.commit()
    conn.close()
    return retur



@app.route('/metries')
def index():
    date = str(datetime.date.today() - datetime.timedelta(days=1))

    Successful_requests = make_query('Select Succesful_requests from Metries_int where Date ="' + date + '"')[0][0]
    Unique_users = make_query('Select Unq_users from Metries_int where Date ="' + date + '"')[0][0]
    Countries = make_query('Select Countries from Metries_int where Date ="' + date + '"')[0][0]
    Today_users = make_query('Select Today_users from Metries_int where Date ="' + date + '"')[0][0]
    Visitings_of_the_most_visited_page = make_query('Select Visiting_most_visited_page from Metries_int where Date ="' + date + '"')[0][0]
    Top_requests_hour = make_query('Select Top_requests_hour from Metries_int where Date ="' + date + '"')[0][0]
    Top_unique_users_hour = make_query('Select Top_unique_users_hour from Metries_int where Date ="' + date + '"')[0][0]
    Unique_outgoing_sites = make_query('Select Unq_outgoing_sites from Metries_int where Date ="' + date + '"')[0][0]
    English_translatings = make_query('Select Russian_translatings from Metries_int where Date ="' + date + '"')[0][0]

    Unique_users_per_country3 = make_query('Select Unq_users_per_country from Metries_countries where Date ="' + date + '"')[0][0]
    Unique_users_per_country2 = Unique_users_per_country3.strip().split(';')
    flag = False
    Unique_users_per_country = {}
    for i in range(len(Unique_users_per_country2) - 1):
        Unique_users_per_country1 = Unique_users_per_country2[i].strip().split('-')
        if flag == False:
            Unique_users_per_country['?'] = Unique_users_per_country1[1]
            flag = True
        else:
            Unique_users_per_country[Unique_users_per_country1[0]] = Unique_users_per_country1[1]

    Requests_per_country3 = make_query('Select Requests_per_country from Metries_countries where Date ="' + date + '"')[0][0]
    Requests_per_country2 = Requests_per_country3.strip().split(';')
    flag = False
    Requests_per_country = {}
    for i in range(len(Requests_per_country2) - 1):
        Requests_per_country1 = Requests_per_country2[i].strip().split('-')
        if flag == False:
            Requests_per_country['?'] = Requests_per_country1[1]
            flag = True
        else:
            Requests_per_country[Requests_per_country1[0]] = Requests_per_country1[1]

    Average_num_of_requests_per_country3 = make_query('Select Average_num_of_requests_per_country from Metries_countries where Date ="' + date + '"')[0][0]
    Average_num_of_requests_per_country2 = Average_num_of_requests_per_country3.strip().split(';')
    flag = False
    Average_num_of_requests_per_country = {}
    for i in range(len(Average_num_of_requests_per_country2) - 1):
        Average_num_of_requests_per_country1 = Average_num_of_requests_per_country2[i].strip().split('-')
        if flag == False:
            Average_num_of_requests_per_country['?'] = Average_num_of_requests_per_country1[1]
            flag = True
        else:
            Average_num_of_requests_per_country[Average_num_of_requests_per_country1[0]] = Average_num_of_requests_per_country1[1]

    result = {'metries': {'int': {'Successful_requests': Successful_requests,
                                  'Unique_users': Unique_users,
                                  'Countries': Countries,
                                  'Today_users': Today_users,
                                  'Visitings_of_the_most_visited_page': Visitings_of_the_most_visited_page,
                                  'Top_requests_hour': Top_requests_hour,
                                  'Top_unique_users_hour': Top_unique_users_hour,
                                  'Unique_outgoing_sites': Unique_outgoing_sites,
                                  'English_translatings': English_translatings},
                          'str':{'Unique_users_per_country':Unique_users_per_country,
                                  'Requests_per_country': Requests_per_country,
                                  'Average_num_of_requests_per_country':Average_num_of_requests_per_country}}}

    return jsonify(result)


@app.route('/metries_tommorow')

if __name__ == '__main__':
    app.run('194.87.92.210', 234, debug=True)
 

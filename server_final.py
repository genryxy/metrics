
# coding: utf-8

# In[ ]:


import sys
sys.path.append('.localpip')
from flask import Flask, jsonify, abort, make_response
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


def stroka(date):
    Unique_users_per_country3 = make_query('Select Unq_users_per_country from Metries_countries where Date ="' + date + '"')[0][0]
    Unique_users_per_country2 = Unique_users_per_country3.strip().split(';')
    flag = False
    Unique_users_per_country = {}
    for i in range(len(Unique_users_per_country2) - 1):
        Unique_users_per_country1 = Unique_users_per_country2[i].strip().split('-')
        if flag == False:
            Unique_users_per_country['?'] = int(Unique_users_per_country1[1])
            flag = True
        else:
            Unique_users_per_country[Unique_users_per_country1[0]] = int(Unique_users_per_country1[1])

    Requests_per_country3 = make_query('Select Requests_per_country from Metries_countries where Date ="' + date + '"')[0][0]
    Requests_per_country2 = Requests_per_country3.strip().split(';')
    flag = False
    Requests_per_country = {}
    for i in range(len(Requests_per_country2) - 1):
        Requests_per_country1 = Requests_per_country2[i].strip().split('-')
        if flag == False:
            Requests_per_country['?'] = int(Requests_per_country1[1])
            flag = True
        else:
            Requests_per_country[Requests_per_country1[0]] = int(Requests_per_country1[1])

    Average_num_of_requests_per_country3 = make_query('Select Average_num_of_requests_per_country from Metries_countries where Date ="' + date + '"')[0][0]
    Average_num_of_requests_per_country2 = Average_num_of_requests_per_country3.strip().split(';')
    flag = False
    Average_num_of_requests_per_country = {}
    for i in range(len(Average_num_of_requests_per_country2) - 1):
        Average_num_of_requests_per_country1 = Average_num_of_requests_per_country2[i].strip().split('-')
        if flag == False:
            Average_num_of_requests_per_country['?'] = float(Average_num_of_requests_per_country1[1])
            flag = True
        else:
            Average_num_of_requests_per_country[Average_num_of_requests_per_country1[0]] = float(Average_num_of_requests_per_country1[1])

    return Unique_users_per_country, Requests_per_country, Average_num_of_requests_per_country


def chislo(date):
    Successful_requests = make_query('Select Successful_requests from Metries_int where Date ="' + date + '"')[0][0]
    Unique_users = make_query('Select Unq_users from Metries_int where Date ="' + date + '"')[0][0]
    Countries = make_query('Select Countries from Metries_int where Date ="' + date + '"')[0][0]
    Today_users = make_query('Select Today_users from Metries_int where Date ="' + date + '"')[0][0]
    Visitings_of_the_most_visited_page = make_query('Select Visiting_most_visited_page from Metries_int where Date ="' + date + '"')[0][0]
    Top_requests_hour = make_query('Select Top_requests_hour from Metries_int where Date ="' + date + '"')[0][0]
    Top_unique_users_hour = make_query('Select Top_unique_users_hour from Metries_int where Date ="' + date + '"')[0][0]
    Unique_outgoing_sites = make_query('Select Unq_outgoing_sites from Metries_int where Date ="' + date + '"')[0][0]
    English_translatings = make_query('Select English_translatings from Metries_int where Date ="' + date + '"')[0][0]

    return Successful_requests, Unique_users, Countries, Today_users, Visitings_of_the_most_visited_page, Top_requests_hour, Top_unique_users_hour, Unique_outgoing_sites, English_translatings


def check_error(result):
    if len(result) == 0:
        abort(404)
    else:
        return jsonify(result)
    
    
@app.route('/metries')
def index():
    d = datetime.datetime.today() - datetime.timedelta(days=1, hours=4, minutes=16)
    date = str(datetime.date(d.year, d.month, d.day))

    Successful_requests, Unique_users, Countries, Today_users, Visitings_of_the_most_visited_page, Top_requests_hour, Top_unique_users_hour, Unique_outgoing_sites, English_translatings = chislo(date)

    Unique_users_per_country, Requests_per_country, Average_num_of_requests_per_country = stroka(date)
    

    result = {'metries': {'Date':date,
                          'int': {'Successful_requests': Successful_requests,
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

    get_error(result)


@app.route('/metries/<types>')
def index2(types):
    d = datetime.datetime.today() - datetime.timedelta(days=1, hours=4, minutes=16)
    date = str(datetime.date(d.year, d.month, d.day))
    if types == 'suc_req':
        Successful_requests = make_query('Select Successful_requests from Metries_int where Date ="' + date + '"')[0][0]
        result = {'Date':date, 'Successful_requests': Successful_requests}
        check_error(result)
    elif types == 'unq_us':
        Unique_users = make_query('Select Unq_users from Metries_int where Date ="' + date + '"')[0][0]
        result = {'Date':date, 'Unique_users': Unique_users}
        check_error(result)
    elif types == 'countries':
        Countries = make_query('Select Countries from Metries_int where Date ="' + date + '"')[0][0]
        result = {'Date':date, 'Countries': Countries}
        check_error(result)
    elif types == 'tod_us':
        Today_users = make_query('Select Today_users from Metries_int where Date ="' + date + '"')[0][0]
        result = {'Date':date, 'Today_users': Today_users}
        check_error(result)
    elif types == 'Vis_vis_page':
        Visitings_of_the_most_visited_page = make_query('Select Visiting_most_visited_page from Metries_int where Date ="' + date + '"')[0][0]
        result = {'Date':date, 'Visitings_of_the_most_visited_page': Visitings_of_the_most_visited_page}
        check_error(result)
    elif types == 'top_req_h':
        Top_requests_hour = make_query('Select Top_requests_hour from Metries_int where Date ="' + date + '"')[0][0]
        result = {'Date':date, 'Top_requests_hour': Top_requests_hour}
        check_error(result)
    elif types == 'top_unq_us_h':
        Top_unique_users_hour = make_query('Select Top_unique_users_hour from Metries_int where Date ="' + date + '"')[0][0]
        result = {'Date':date, 'Top_unique_users_hour': Top_unique_users_hour}
        check_error(result)
    elif types == 'unq_og_sites':
        Unique_outgoing_sites = make_query('Select Unq_outgoing_sites from Metries_int where Date ="' + date + '"')[0][0]
        result = {'Date':date, 'Unique_outgoing_sites': Unique_outgoing_sites}
        check_error(result)
    elif types == 'eng_trans':
        English_translatings = make_query('Select English_translatings from Metries_int where Date ="' + date + '"')[0][0]
        result = {'Date':date, 'English_translatings': English_translatings}
        check_error(result)

    elif types == 'unq_us_country':
        Unique_users_per_country3 = make_query('Select Unq_users_per_country from Metries_countries where Date ="' + date + '"')[0][0]
        Unique_users_per_country2 = Unique_users_per_country3.strip().split(';')
        flag = False
        Unique_users_per_country = {}
        for i in range(len(Unique_users_per_country2) - 1):
            Unique_users_per_country1 = Unique_users_per_country2[i].strip().split('-')
            if flag == False:
                Unique_users_per_country['?'] = int(Unique_users_per_country1[1])
                flag = True
            else:
                Unique_users_per_country[Unique_users_per_country1[0]] = int(Unique_users_per_country1[1])
        result = {'Date':date, 'Unique_users_per_country': Unique_users_per_country}
        check_error(result)

    elif types == 'req_country':
        Requests_per_country3 = make_query('Select Requests_per_country from Metries_countries where Date ="' + date + '"')[0][0]
        Requests_per_country2 = Requests_per_country3.strip().split(';')
        flag = False
        Requests_per_country = {}
        for i in range(len(Requests_per_country2) - 1):
            Requests_per_country1 = Requests_per_country2[i].strip().split('-')
            if flag == False:
                Requests_per_country['?'] = int(Requests_per_country1[1])
                flag = True
            else:
                Requests_per_country[Requests_per_country1[0]] = int(Requests_per_country1[1])
        result = {'Date':date, 'Requests_per_country': Requests_per_country}
        check_error(result)

    elif types == 'ave_req_country':
        Average_num_of_requests_per_country3 = make_query('Select Average_num_of_requests_per_country from Metries_countries where Date ="' + date + '"')[0][0]
        Average_num_of_requests_per_country2 = Average_num_of_requests_per_country3.strip().split(';')
        flag = False
        Average_num_of_requests_per_country = {}
        for i in range(len(Average_num_of_requests_per_country2) - 1):
            Average_num_of_requests_per_country1 = Average_num_of_requests_per_country2[i].strip().split('-')
            if flag == False:
                Average_num_of_requests_per_country['?'] = float(Average_num_of_requests_per_country1[1])
                flag = True
            else:
                Average_num_of_requests_per_country[Average_num_of_requests_per_country1[0]] = float(Average_num_of_requests_per_country1[1])
        result = {'Date':date, 'Average_num_of_requests_per_country': Average_num_of_requests_per_country}
        check_error(result)

    elif types == 'int':
        Successful_requests, Unique_users, Countries, Today_users, Visitings_of_the_most_visited_page, Top_requests_hour, Top_unique_users_hour, Unique_outgoing_sites, English_translatings = chislo(date)

        result = {'Date':date, 
                  'int': {'Successful_requests': Successful_requests,
                          'Unique_users': Unique_users,
                          'Countries': Countries,
                          'Today_users': Today_users,
                          'Visitings_of_the_most_visited_page': Visitings_of_the_most_visited_page,
                          'Top_requests_hour': Top_requests_hour,
                          'Top_unique_users_hour': Top_unique_users_hour,
                          'Unique_outgoing_sites': Unique_outgoing_sites,
                          'English_translatings': English_translatings}}
        check_error(result)

    elif types == 'str':
        Unique_users_per_country, Requests_per_country, Average_num_of_requests_per_country = stroka(date)

        result = {'Date':date, 
                  'str': {'Unique_users_per_country': Unique_users_per_country,
                          'Requests_per_country': Requests_per_country,
                          'Average_num_of_requests_per_country': Average_num_of_requests_per_country}}
        check_error(result)

    else:
        abort(404)

@app.route('/metries_yesterday')
def index3():
    d = datetime.datetime.today() - datetime.timedelta(days=2, hours=4, minutes=16)
    date = str(datetime.date(d.year, d.month, d.day))

    Successful_requests, Unique_users, Countries, Today_users, Visitings_of_the_most_visited_page, Top_requests_hour, Top_unique_users_hour, Unique_outgoing_sites, English_translatings = chislo(date)

    Unique_users_per_country, Requests_per_country, Average_num_of_requests_per_country = stroka(date)

    result = {'metries': {'Date':date, 
                          'int': {'Successful_requests': Successful_requests,
                                  'Unique_users': Unique_users,
                                  'Countries': Countries,
                                  'Today_users': Today_users,
                                  'Visitings_of_the_most_visited_page': Visitings_of_the_most_visited_page,
                                  'Top_requests_hour': Top_requests_hour,
                                  'Top_unique_users_hour': Top_unique_users_hour,
                                  'Unique_outgoing_sites': Unique_outgoing_sites,
                                  'English_translatings': English_translatings},
                          'str': {'Unique_users_per_country':Unique_users_per_country,
                                  'Requests_per_country': Requests_per_country,
                                  'Average_num_of_requests_per_country':Average_num_of_requests_per_country}}}
    check_error(result)

@app.route('/metries_yesterday/<types>')
def index4(types):
    d = datetime.datetime.today() - datetime.timedelta(days=2, hours=4, minutes=16)
    date = str(datetime.date(d.year, d.month, d.day))

    if types == 'suc_req':
        Successful_requests = make_query('Select Successful_requests from Metries_int where Date ="' + date + '"')[0][0]
        result = {'Date':date, 'Successful_requests':Successful_requests}
        check_error(result)
    elif types == 'unq_us':
        Unique_users = make_query('Select Unq_users from Metries_int where Date ="' + date + '"')[0][0]
        result = {'Date':date, 'Unique_users':Unique_users}
        check_error(result)
    elif types == 'countries':
        Countries = make_query('Select Countries from Metries_int where Date ="' + date + '"')[0][0]
        result = {'Date':date, 'Countries':Countries}
        check_error(result)
    elif types == 'tod_us':
        Today_users = make_query('Select Today_users from Metries_int where Date ="' + date + '"')[0][0]
        result = {'Date':date, 'Today_users':Today_users}
        check_error(result)
    elif types == 'Vis_vis_page':
        Visitings_of_the_most_visited_page = make_query('Select Visiting_most_visited_page from Metries_int where Date ="' + date + '"')[0][0]
        result = {'Date':date, 'Visitings_of_the_most_visited_page':Visitings_of_the_most_visited_page}
        check_error(result)
    elif types == 'top_req_h':
        Top_requests_hour = make_query('Select Top_requests_hour from Metries_int where Date ="' + date + '"')[0][0]
        result = {'Date':date, 'Top_requests_hour':Top_requests_hour}
        check_error(result)
    elif types == 'top_unq_us_h':
        Top_unique_users_hour = make_query('Select Top_unique_users_hour from Metries_int where Date ="' + date + '"')[0][0]
        result = {'Date':date, 'Top_unique_users_hour':Top_unique_users_hour}
        check_error(result)
    elif types == 'unq_og_sites':
        Unique_outgoing_sites = make_query('Select Unq_outgoing_sites from Metries_int where Date ="' + date + '"')[0][0]
        result = {'Date':date, 'Unique_outgoing_sites':Unique_outgoing_sites}
        check_error(result)
    elif types == 'eng_trans':
        English_translatings = make_query('Select English_translatings from Metries_int where Date ="' + date + '"')[0][0]
        result = {'Date':date, 'English_translatings':English_translatings}
        check_error(result)

    elif types == 'unq_us_country':
        Unique_users_per_country3 = make_query('Select Unq_users_per_country from Metries_countries where Date ="' + date + '"')[0][0]
        Unique_users_per_country2 = Unique_users_per_country3.strip().split(';')
        flag = False
        Unique_users_per_country = {}
        for i in range(len(Unique_users_per_country2) - 1):
            Unique_users_per_country1 = Unique_users_per_country2[i].strip().split('-')
            if flag == False:
                Unique_users_per_country['?'] = int(Unique_users_per_country1[1])
                flag = True
            else:
                Unique_users_per_country[Unique_users_per_country1[0]] = int(Unique_users_per_country1[1])
        result = {'Date':date, 'Unique_users_per_country':Unique_users_per_country}
        check_error(result)

    elif types == 'req_country':
        Requests_per_country3 = make_query('Select Requests_per_country from Metries_countries where Date ="' + date + '"')[0][0]
        Requests_per_country2 = Requests_per_country3.strip().split(';')
        flag = False
        Requests_per_country = {}
        for i in range(len(Requests_per_country2) - 1):
            Requests_per_country1 = Requests_per_country2[i].strip().split('-')
            if flag == False:
                Requests_per_country['?'] = int(Requests_per_country1[1])
                flag = True
            else:
                Requests_per_country[Requests_per_country1[0]] = int(Requests_per_country1[1])
        result = {'Date':date, 'Requests_per_country':Requests_per_country}
        check_error(result)

    elif types == 'ave_req_country':
        Average_num_of_requests_per_country3 = make_query('Select Average_num_of_requests_per_country from Metries_countries where Date ="' + date + '"')[0][0]
        Average_num_of_requests_per_country2 = Average_num_of_requests_per_country3.strip().split(';')
        flag = False
        Average_num_of_requests_per_country = {}
        for i in range(len(Average_num_of_requests_per_country2) - 1):
            Average_num_of_requests_per_country1 = Average_num_of_requests_per_country2[i].strip().split('-')
            if flag == False:
                Average_num_of_requests_per_country['?'] = float(Average_num_of_requests_per_country1[1])
                flag = True
            else:
                Average_num_of_requests_per_country[Average_num_of_requests_per_country1[0]] = float(Average_num_of_requests_per_country1[1])
        result = {'Date':date, 'Average_num_of_requests_per_country':Average_num_of_requests_per_country}
        check_error(result)

    elif types == 'int':
        Successful_requests, Unique_users, Countries, Today_users, Visitings_of_the_most_visited_page, Top_requests_hour, Top_unique_users_hour, Unique_outgoing_sites, English_translatings = chislo(date)

        result = {'Date':date, 
                  'int':{'Successful_requests': Successful_requests,
                         'Unique_users': Unique_users,
                         'Countries': Countries,
                         'Today_users': Today_users,
                         'Visitings_of_the_most_visited_page': Visitings_of_the_most_visited_page,
                         'Top_requests_hour': Top_requests_hour,
                         'Top_unique_users_hour': Top_unique_users_hour,
                         'Unique_outgoing_sites': Unique_outgoing_sites,
                         'English_translatings': English_translatings}}
        check_error(result)

    elif types == 'str':

        Unique_users_per_country, Requests_per_country, Average_num_of_requests_per_country = stroka(date)

        result = {'Date':date, 
                  'str':{'Unique_users_per_country':Unique_users_per_country,
                         'Requests_per_country': Requests_per_country,
                         'Average_num_of_requests_per_country':Average_num_of_requests_per_country}}
        check_error(result)

    else:
        abort(404)

@app.route('/metries_all')
def index5():
    t = make_query("select * from Metries_int")

    d = datetime.datetime.today() - datetime.timedelta(days=1, hours=4, minutes=16)
    date_t = str(datetime.date(d.year, d.month, d.day))

    date = []
    suc_req = []
    countries = []
    unq_users = []
    today_users = []
    visiting_most = []
    top_hour = []
    top_unique_hour = []
    unq_outgoing_sites = []
    number_translatings = []

    for i in t:
        date.append(i[0])
        suc_req.append(i[1])
        unq_users.append(i[2])
        countries.append(i[3])
        today_users.append(i[4])
        visiting_most.append(i[5])
        top_hour.append(i[6])
        top_unique_hour.append(i[7])
        unq_outgoing_sites.append(i[8])
        number_translatings.append(i[9])

    suc_req = [str(i) for i in suc_req]
    unq_users = [str(i) for i in unq_users]
    countries = [str(i) for i in countries]
    today_users = [str(i) for i in today_users]
    visiting_most = [str(i) for i in visiting_most]
    top_hour = [str(i) for i in top_hour]
    top_unique_hour = [str(i) for i in top_unique_hour]
    unq_outgoing_sites = [str(i) for i in unq_outgoing_sites]
    number_translatings = [str(i) for i in number_translatings]

    date_str = date[0] + ' - ' + date[len(date) - 1]
    suc_req_str = ', '.join(suc_req)
    unq_users_str = ', '.join(unq_users)
    countries_str = ', '.join(countries)
    today_users_str = ', '.join(today_users)
    visiting_most_str = ', '.join(visiting_most)
    top_hour_str = ', '.join(top_hour)
    top_unique_hour_str = ', '.join(top_unique_hour)
    unq_outgoing_sites_str = ', '.join(unq_outgoing_sites)
    number_translatings_str = ', '.join(number_translatings)

    Unique_users_per_country, Requests_per_country, Average_num_of_requests_per_country = stroka(date_t)

    result = {'metries':
                        {'int':{'Date': date_str,
                                'Successful_requests': suc_req_str,
                                'Unique_users': unq_users_str,
                                'Countries': countries_str,
                                'Today_users': today_users_str,
                                'Visitings_of_the_most_visited_page': visiting_most_str,
                                'Top_requests_hour': top_hour_str,
                                'Top_unique_users_hour': top_unique_hour_str,
                                'Unique_outgoing_sites': unq_outgoing_sites_str,
                                'English_translatings': number_translatings_str},
                        'str': {'Date': date[len(date)-1],
                                'Unique_users_per_country': Unique_users_per_country,
                                'Requests_per_country': Requests_per_country,
                                'Average_num_of_requests_per_country': Average_num_of_requests_per_country}}}

    check_error(result)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run('194.87.92.210', 234, debug=True)


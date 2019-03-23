#!/usr/bin/python3

try:
    from urllib.parse import urlencode
    from requests import get, HTTPError
    from subprocess import run
    from time import time, localtime, strftime
    import psycopg2 as psql
    from json import loads, dumps
    from os.path import exists
    from datetime import datetime
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


def database_inflater(data):
    # fetched data is put into local postgresql database
    # database and table are already created, make sure you've done so properly
    try:
        db = psql.connect(database='nasa_apod', user='postgres', password='password')
        db_cursor = db.cursor()
        db_cursor.execute('insert into apod_data values(%s, %s, %s, %s, %s, %s, %s, %s)', (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))
        db.commit()
        db_cursor.close()
        db.close()
    except psql.DatabaseError as e:
        print('[!]Error : {}'.format(str(e)))
        db.close()
        return False
    except Exception as e:
        print('[!]Error : {}'.format(str(e)))
        db.close()
        return False
    return True


def fetch_apod(url, date, api_key, hd=False):
    # date should be in yyyy-mm-dd format
    # if hd image link is required only, then put hd parameter as True
    try:
        final_url = '{0}?{1}'.format(url, urlencode({'date': date, 'api_key': api_key}))
        resp = get(final_url)
    except HTTPError as e:
        print('[!]Error : {}'.format(str(e)))
        exit(1)
    except Exception as e:
        print('[!]Error : {}'.format(str(e)))
        exit(1)
    if(resp.status_code != 200):
        print('[!]Error : {}'.format(resp.json().get('msg')))
        if(resp.headers.get('X-RateLimit-Remaining') == '0'):
            nextToStartFrom(date)
            exit(1)
        return ()
    else:
        data = resp.json()
        if(database_inflater([data.get('date'), data.get('copyright', 'NA'), data.get('explanation', 'NA'), data.get('hdurl', 'NA'), data.get('media_type', 'NA'), data.get('service_version', 'NA'), data.get('title', 'NA'), data.get('url', 'NA')])):
            print('\t[+]Stored in database :)\n')
    return (resp.headers.get('X-RateLimit-Remaining'), resp.headers.get('X-RateLimit-Limit'))


def config_reader(filename='config.json'):
    # reads config file and gets those data, which are kept pretty much unchanged
    data = ''
    try:
        with open(filename, 'r') as fd:
            data = fd.read()
        data = loads(data)
    except FileNotFoundError as e:
        print('[!]Error : {}'.format(str(e)))
        data = {}
    except Exception as e:
        print('[!]Error : {}'.format(str(e)))
        data = {}
    return data


def nextToStartFrom(nextStartDate, filename='nextStart.json'):
    # stores record in local json file, where to start from next
    try:
        with open(filename, 'w') as fd:
            fd.write(dumps({'date': nextStartDate}))
    except FileNotFoundError as e:
        print('[!]Error : {}'.format(str(e)))
        return False
    except Exception as e:
        print('[!]Error : {}'.format(str(e)))
        return False
    return True


def getTimeFromString(dateTime):
    date = dateTime.split('-')
    return datetime(int(date[0]), int(date[1]), int(date[2])).timestamp()


def getStopDate():
    # gives back last date of which we've a record stored in database
    date = ()
    try:
        db = psql.connect(database='nasa_apod', user='postgres', password='@njan5m3dB')
        db_cursor = db.cursor()
        db_cursor.execute('select date from apod_data order by date desc')
        date = db_cursor.fetchone()
        db_cursor.close()
        db.close()
    except psql.DatabaseError as e:
        print('[!]Error : {}'.format(str(e)))
        db.close()
        return ''
    except Exception as e:
        print('[!]Error : {}'.format(str(e)))
        db.close()
        return ''
    if(date):
        return date[0]
    return ''


def app():
    # app starts running here
    run('clear')
    config = config_reader()
    api_key = config.get('api_key')
    targetURL = config.get('target_url')
    startDate = config.get('start_date')
    currentDate = strftime('%Y-%m-%d', localtime(time()))
    if(exists('nextStart.json')):
        next = config_reader(filename='nextStart.json')
        currentDate = next.get('date')
    rateLimit = 1000
    rateRemaining = 1000
    while(currentDate != startDate):
        print('[+]Fetching data from NASA for {} ... {} / {}\n'.format(currentDate, rateRemaining, rateLimit))
        resp = fetch_apod(targetURL, currentDate, api_key)
        currentDate = strftime('%Y-%m-%d', localtime(getTimeFromString(currentDate) - 24*3600))
        if(resp):
            rateRemaining = resp[0]
            rateLimit = resp[1]
    nextToStartFrom(strftime('%Y-%m-%d', localtime(time() + 24*3600)))
    return


if __name__ == '__main__':
    try:
        app()
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)

#!/usr/bin/python3

try:
    from apod_downloader import getStopDate, getTimeFromString, config_reader, run, localtime, time, strftime, fetch_apod
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


def app():
    # once you've completed inflating database, try executing this file,
    # which will only update database by latest release from NASA APOD.
    run('clear')
    config = config_reader()
    api_key = config.get('api_key')
    targetURL = config.get('target_url')
    currentDate = strftime('%Y-%m-%d', localtime(time()))
    stopDate = getStopDate()
    if(not stopDate):
        print('[!]First inflate database by running apod_downloader.py.\n')
        return
    rateLimit = 1000
    rateRemaining = 1000
    while(currentDate != stopDate):
        print('[+]Fetching data from NASA for {} ... {} / {}\n'.format(currentDate, rateRemaining, rateLimit))
        resp = fetch_apod(targetURL, currentDate, api_key)
        currentDate = strftime('%Y-%m-%d', localtime(getTimeFromString(currentDate) - 24*3600))
        if(resp):
            rateRemaining = resp[0]
            rateLimit = resp[1]
    return


if __name__ == '__main__':
    try:
        app()
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
# apod_fetcher
A Pythonic wayout to fetch Astronomy Picture of the Day from NASA and populate Database.


## Documentation ::

  1. A Local PostgreSQL Database is already setup, which will get populated by [apod_downloader.py](https://github.com/itzmeanjan/apod_fetcher/blob/master/apod_downloader.py) and [apod_updater.py](https://github.com/itzmeanjan/apod_fetcher/blob/master/apod_updater.py), these two scripts. Setup your local SQL database as below.
  
   ```
    nasa_apod=# \d apod_data
                         Table "public.apod_data"
     Column      |         Type          | Collation | Nullable | Default 
-----------------+-----------------------+-----------+----------+---------
 date            | character(10)         |           | not null | 
 copyright       | text                  |           |          | 
 explanation     | text                  |           |          | 
 hdurl           | text                  |           |          | 
 media_type      | character varying(25) |           |          | 
 service_version | character varying(10) |           |          | 
 title           | text                  |           |          | 
 url             | text                  |           |          | 

   ```
  
  2. Remember, you need to first run [apod_downloader.py](https://github.com/itzmeanjan/apod_fetcher/blob/master/apod_downloader.py) and you have to run this script repeatedly until it downloads all **APODs** till date. This might be painful.
  
  3. NASA API will let you download only 1000 APODs per hour.
  
  4. Once you complete downloading all APODs, next time simply run [apod_updater.py](https://github.com/itzmeanjan/apod_fetcher/blob/master/apod_updater.py), which will fetch APODs of missing dates, starting from current date.
  
  5. You need to run this script every 24 hours, in repeated fashion.
  
  6. NASA updates APOD following US Time( not sure which one), so make sure, you run the script only when it's time. Otherwise you might encounter some kind of unexpected response.
  
  
*You might be interested in checking out this [repo](https://github.com/itzmeanjan/apod_server), which is an implementation of Express App, that fetches APOD by date.*
 
That's it. Hope it was helpful :)

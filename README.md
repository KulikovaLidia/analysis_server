# analysis_server
Thank you for choosing analysis_server service - a service to analyze a birthday gifts demand by month.

## Installation 
Install dependencies with pip:

```$ pip install -r requirements.txt```

## Run analysis_server

### Run analysis_server locally
```$ python3 app.py```

### Run analysis_server for production on 4 workers
```$ gunicorn app:app -w 4 -b 0.0.0.0:8080```

Use supervisor to manage the process(monitor state, restart, etc.)


## URL examples

* Add a new citizen import:\
```POST http://0.0.0.0:8080/imports```
* Update a citizen in an import:\
```PATCH http://0.0.0.0:8080/imports/<import_id>/citizens/<citizen_id>```
* Get all citizens in an inmport:\
```GET http://0.0.0.0:8080/imports/<import_id>/citizens```
* Get presents number grouped by a citizen by months:\
```GET http://0.0.0.0:8080/imports/<import_id>/citizens/birthdays```

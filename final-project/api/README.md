# REST API Module 
### Main Dev: Abid Ahmed

## Frameworks and Tools:
    - Django REST Framework
    - Postgresql
    - Firebase Authentication
    - Celery
    - Redis

## Important API Files
Every API endpoint is handled by an app. Use the following command to create an app.
```
python manage.py startapp <app_name>
```
Every time an app is created, it needs to be added to the INSTALLED_APPS list in moth_api/moth_api/settings.py. Each app contains the following files:
* models.py
    * Defines database entries relating to the app
    * To make updates and changes to the database, run the following
    ```
    python manage.py makemigrations <app_name>
    python manage.py migrate <app_name>
    ```
    * The database table relating to the model will be labeled as <app_name>_<model_name>
* serializers.py
    * Manages the serialization and deserialization (formatting) of the JSON data
    * The fields variable defines what variables the API returns
* views.py
    * Handles the CRUD (Create, Retrieve, Update, Delete) logic when a client connects to a specific endpoint
* permissions.py
    * Contains custom permissions relating to the app (if needed)
* services.py
    * Contains services (custom functionality for the app) relevant to the app

The api app holds the API together. Thus, it has a different functionality than other apps and does not follow the traditional convention described above. This app handles the views and endpoints for calls to the API.
* api_urls.py 
    * Contains all the url paths for each API endpoint. Each endpoint defines how the API responds when a client sends a HTTP request
* views.py
    * This lists/defines the entry points for the API

After the above files for a regular app are written, do the following steps to make each app accessible to the client:
1) Add the relevant url patterns for this app to moth_api/api/api_urls.py
2) If an app needs to have an entry point, add it to the API root by following the convention defined in moth_api/api/views.py

## Running the Web Server
To run the web server, enter the following command
```
python manage.py runserver 0.0.0.0:8000
```
Alternatively, 
```
chmod 777 run.sh (if needed)
./run.sh
```
The API Root is located at 
```
http://167.172.31.118:8000/api/v1/
```
Documentation is located at 
```
http://167.172.31.118:8000/api/v1/docs
```

## Authentication

<u>**Important**</u>: The API only cares about receiving a valid authentication token. Other tasks such as login, registration, password change, etc are relegated to the front end.

The API utilizes Firebase Authentication. Thus, authentication is done by acquiring a token from Firebase. For front-end development, Firebase has libraries to handle acquiring the token and authenticating the user. For testing purposes or if a library cannot be used, the following API call is invoked.

```
POST https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={FIREBASE_API_KEY}
```
**Payload**
```
{
    "email": {email},
    "password": {password},
    "returnSecureToken: true,
}
```

The ```id_token``` field is the authentication token. The ```localId``` field is the user's UID for Firebase and the Moth Classifier API. To authenticate with the Moth Classifier API, use that token as a Bearer token when forming the request. 

## Celery
Celery is used to handle and execute jobs asynchronously. Documentation for Celery can be found [here](https://docs.celeryproject.org/en/stable/). 

To start the scheduler,
```
celery -A moth_api beat -l info
```

To start the worker,
```
celery -A moth_api worker -l info
```

In the future (in a production environment) these will be daemonized.

## Redis Pub/Sub
Redis, specifically ```redis-py```, is used to handle the publish/subscribe communication between the Moth Classifier API and the Machine Learning service. redis-server must be installed on the Moth Classifier API host machine. Documentation ```redis-py``` can be found [here](https://github.com/andymccurdy/redis-py).

To start/stop/restart the redis server,
```
/etc/init.d/redis-server {start/stop/restart}
```

To test the redis server,
```
redis-cli ping
```

The Moth Classifier API has a django management commmand to start listening for responses from the Machine Learning service.
```
python manage.py ml_subscribe
```

In the future (in a production environment) this will be daemonized.

The Machine Learning service has a handler program that subscribes to the API to get new jobs and publishes completed jobs to the API.
```
python api_handler.py
```

In the future (in a production environment) this will be daemonized.
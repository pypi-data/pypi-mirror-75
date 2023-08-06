![POLITICO](https://rawgithub.com/The-Politico/src/master/images/logo/badge.png)

# politico-civic-election-loader

Ingest election metadata and results from outside sources, the POLITICO way.


## Quickstart

1. Install the app.

  ```
  $ pip install politico-civic-election-loader
  ```

2. Add the app to your Django project settings.

  ```python
  INSTALLED_APPS = [
      # ...
      'rest_framework',
      'election_loader',
  ]
  ```

3. Migrate the database.

  ```
  $ python manage.py migrate entity
  ```


## Developing

### Running a development server

Move into the example directory, install dependencies and run the development server with pipenv.

  ```
  $ cd example
  $ pipenv install
  $ pipenv run python manage.py runserver
  ```

### Setting up a PostgreSQL database

1. Run the make command to setup a fresh database.

  ```
  $ make database
  ```

2. Add a connection URL to `example/.env`.

  ```
  DATABASE_URL="postgres://localhost:5432/electionloader"
  ```

3. Run migrations from the example app.

  ```
  $ cd example
  $ pipenv run python manage.py migrate
  ```


## Copyright

&copy; 2019&ndash;present POLITICO, LLC

![POLITICO](https://rawgithub.com/The-Politico/src/master/images/logo/badge.png)

# django-politico-minutes-edition

### Quickstart

1. Install the app.

  ```
  $ pip install django-politico-minutes-edition
  ```

2. Add the app to your Django project and configure settings.

  ```python
  INSTALLED_APPS = [
      # ...
      'rest_framework',
      'minutes',
  ]

  #########################
  # minutes settings

  MINUTES_SECRET_KEY = ''
  MINUTES_AWS_ACCESS_KEY_ID = ''
  MINUTES_AWS_SECRET_ACCESS_KEY = ''
  MINUTES_AWS_REGION = ''
  MINUTES_AWS_S3_BUCKET = ''
  MINUTES_CLOUDFRONT_ALTERNATE_DOMAIN = ''
  MINUTES_S3_UPLOAD_ROOT = ''
  ```

### Developing

##### Running a development server

Developing python files? Move into example directory and run the development server with pipenv.

  ```
  $ cd example
  $ pipenv run python manage.py runserver
  ```

Developing static assets? Move into the pluggable app's staticapp directory and start the node development server, which will automatically proxy Django's development server.

  ```
  $ cd minutes/staticapp
  $ gulp
  ```

Want to not worry about it? Use the shortcut make command.

  ```
  $ make dev
  ```

##### Setting up a PostgreSQL database

1. Run the make command to setup a fresh database.

  ```
  $ make database
  ```

2. Add a connection URL to the `.env` file.

  ```
  DATABASE_URL="postgres://localhost:5432/minutes"
  ```

3. Run migrations from the example app.

  ```
  $ cd example
  $ pipenv run python manage.py migrate
  ```
  
### Development Schedule
- Finish front-end design — (Lily) — 12/4
- Finish Minutes CMS Phase 1 — (Briz) — 12/13
- Content prototyping — (Ryan) — Starts 12/16
- Figure out deploy strategy — (Briz) — 12/20
- Finish Minutes front-end Phase 1 — (Briz/McGill if necessary)) — 1/9
- Front-end/CMS tweaks after content prototyping — (Briz) — 1/16
- Figure out newsletter signup thing — (Briz, McGill, Ali)  — 1/16
- Deploy — (Briz) — 1/21

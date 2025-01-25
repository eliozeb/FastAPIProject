@echo off
echo === Setting up Heroku PostgreSQL ===

REM Set app name
SET APP_NAME=fastapi-elias
SET DATABASE_HOSTNAME=localhost
SET DATABASE_PORT=5432
SET DATABASE_PASSWORD=saselias123
SET DATABASE_NAME=fastapi
SET DATABASE_USERNAME=postgres
SET SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
SET ALGORITHM=HS256
SET ACCESS_TOKEN_EXPIRE_MINUTES=30

REM Create PostgreSQL addon (mini tier for eco dynos)
heroku addons:create heroku-postgresql:mini --app %APP_NAME%

REM Get database credentials
heroku config:get DATABASE_URL --app %APP_NAME%

REM Show database info
heroku pg:info --app %APP_NAME%

REM Set additional config vars
heroku config:set DATABASE_USERNAME=%DATABASE_USERNAME% --app %APP_NAME%
heroku config:set DATABASE_PASSWORD=%DATABASE_PASSWORD% --app %APP_NAME%
heroku config:set DATABASE_NAME=%DATABASE_NAME% --app %APP_NAME%
heroku config:set DATABASE_PORT=%DATABASE_PORT% --app %APP_NAME%
heroku config:set DATABASE_URL=%DB_URL% --app %APP_NAME%
heroku config:set SECRET_KEY=%SECRET_KEY% --app %APP_NAME%
heroku config:set ALGORITHM=%ALGORITHM% --app %APP_NAME%
heroku config:set ACCESS_TOKEN_EXPIRE_MINUTES=%ACCESS_TOKEN_EXPIRE_MINUTES% --app %APP_NAME%

REM Show configuration
heroku config --app %APP_NAME%

echo Database setup complete!
echo on
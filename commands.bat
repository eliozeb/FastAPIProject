@echo off
echo === Setting up Heroku PostgreSQL ===

REM Set app name


REM Create PostgreSQL addon (essential-0 tier for eco dynos)


REM Wait for provision
timeout /t 5

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
heroku pg:info --app %APP_NAME%
heroku config --app %APP_NAME%

echo Database setup complete!
echo on
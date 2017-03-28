# Pycon Nigeria

This is the official website for Python Nigeria Conference

## Setting Up the repo for development
The project uses `python3`

1. Before cloning the repo, create a parent folder

2. clone the repo inside this folder just created 
    ```
    $ git clone https://github.com/pyung/pyconng.git pycon
    # ensure you switch to the develop branch
    $ git checkout develop
    ```

3. Create a virtual environment and activate it 
    ``` 
    $ python -m venv venv
    $ source venv\bin\activate
    $ cd pycon
    
    # for window users
    > venv\Scripts\activate
    ```
4. Install all the dependencies for the project
    ```
    (venv)$ pip install -r requirements/local.txt  
    ```
5. Ensure you have Postgres database installed on your system. visit [Postgres Download Section](https://www.postgresql.org/download/)
to download postgres for your respective OS

6. Create a database using the default `postgres` user and create a db named `pyconng`
    ```
    $ createdb pyconng

    ```
    __This step isn't compulsory if you already have a database that you want to use or you are 
    using `pgadmin3` to create the database.

7. Setup an environmental variable to map the database configuration
    ```
    export DATABASE_URL=postgres://<dbuser>:<dbpassword>@<dbhost>:<dbport>/pyconng
    # remember to set this environment variable
    export DJANGO_SETTINGS_MODULE=config.settings.local
    ```
8. Run migrations
    ```
    python manage.py migrate
    ```
9. Run fixtures (one time only)

    ```bash
    $ python manage.py loaddata fixtures/*
    ```
10. If everything above was successful, you can go ahead and start the server
    ```
    python manage.py runserver
    # if running on cloud9
    python manage.py runserver $IP:$PORT
    ```

# Extras. Useful for frontend developers and designers
For development, the project uses `gulp` and `webpack`

```bash
$ npm install
$ npm run dev #webpack devserver starts.
```
In a new command prompt
```bash
$ gulp watch #Live scss editing
```

## The cloud9 url is at https://ide.c9.io/gbozee/pyconng

## Issue Reporting

If you have found a bug or if you have a feature request, please report them at this repository issues section.

## License
This project is licensed under the MIT license. See the [LICENSE](LICENSE) file for more info.

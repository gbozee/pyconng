# Pycon Nigeria

This is the official website for Python Nigeria Conference

## Setting Up

Enter the directory
```
cd pyconng
```

### Virtual Environment

Install virtualenv via pip
```
pip install virtualenv
```

Create virtualenv
```
virtualenv env
```

Activate virtualenv
```
source ./env/bin/activate
```

_Note_: You can name your virtual environment whatever you want but do not check in your virtual environment to git

### Dependencies

Install the requirements
```
pip install -r requirements.txt
```

### Postgres

Install postgres
```
brew install postgres
```

Create database
```
createdb pyconng
```

Feel free to assign any user credentials to the just created `pyconng` database

### Environment Variables

Specify the below variables
```
export DATABASE_URL="postgres://<dbuser>:<dbpassword>@<dbhost>:<dbport>/pyconng"
```

### Database Setup

Run migrations
```
python manage.py migrate
```
Run fixtures (one time only)

```bash
$ ./manage.py loaddata fixtures/*
```
If everything above was successful, you can go ahead and start the server
```
python manage.py runserver
```

## Extras
For development, the project uses `gulp` and `webpack`

```bash
$ npm install
$ npm run dev #webpack devserver starts.
```
In a new command prompt
```bash
$ gulp watch #Live scss editing
```

## Issue Reporting

If you have found a bug or if you have a feature request, please report them at this repository issues section.

## License

This project is licensed under the MIT license. See the [LICENSE](LICENSE) file for more info.

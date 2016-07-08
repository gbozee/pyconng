# Pycon Nigeria

This is the official website for Python Nigeria Conference

## Setting Up

### Python

Install python from brew
```
brew install python
```

To make sure you have the latest version of Python 2.7.x installed, run this code:
```
brew link python
```

If you get “Already linked” then good to go. Else, run
```
brew unlink python
```
This will remove the old version and link the newly installed version.

### Getting the Code

Clone this repository
```
git clone git@github.com:tsolarin/pyconng.git
```

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

Create a `.env` file in the root of the repository
```
touch .env
```

Specify the below variables
```
export DB_NAME="pyconng"
export DB_USER="<dbuser>"
export DB_PASSWORD="<dbpassword>"
export DB_HOST="<dbhost>"
export DB_PORT="<dbport>"
```

Make variable of your `.env` file available in the current shell session
```
source .env
```

_Note_: Do not check in your `.env` file to git

### Database Setup

Run migrations
```
python manage.py migrate
```

## Usage

If everything above was successful, you can go ahead and start the server
```
python manage.py runserver
```

## Issue Reporting

If you have found a bug or if you have a feature request, please report them at this repository issues section.

## License

This project is licensed under the MIT license. See the [LICENSE](LICENSE) file for more info.

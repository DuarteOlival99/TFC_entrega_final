# tootsie


## How to Install (assuming linux OS)

1. Make a fork in github

2. Setup environment - run the following commands in terminal:
```
mkdir dev
cd dev
git clone https://github.com/your_name/your_fork.git
pipenv shell
pip install Django
pip install --upgrade django-crispy-forms
cd tootsie
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
3. Open browser
```
http://127.0.0.1:8000/
http://127.0.0.1:8000/admin/
```
4. Happy coding


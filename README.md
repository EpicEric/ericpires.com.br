
## Development environment

1. Set the following environment variable in `.bashrc` or `.zshrc` and restart your shell session:

```sh
export DJANGO_DEVELOPMENT=true
```

2. Create a file `main/password.py` with `SECRET_KEY` and `DATABASES` set:

```python
SECRET_KEY = 'your-secret-key-here'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
```

3. Initialize the repository:

```sh
virtualenv venv
source venv/bin/activate
pip install --requirement requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput --link
```

4. Run the development server:

```sh
python manage.py runserver 0.0.0.0:8000
```

5. Access `localhost:8000` in your browser to test the website.


Application for planning astronomy observations and shooting. It allows to import object catalogues (Mesier, Caldwell, custom catalogues ...),
and to calculate which objects will be high enough in the sky during the night and when it will be.

# Setup:

## First time:

```
python3 -m venv myenv
source myenv/bin/activate
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py load_default_catalogues data/default_astronomy_catalogues/Messier.csv --catalogue_name=Messier-default
python3 manage.py load_default_catalogues data/default_astronomy_catalogues/Caldwell.csv --catalogue_name=Caldwell-default
python manage.py runserver
```

## Later:

```
source myenv/bin/activate
python manage.py runserver
```
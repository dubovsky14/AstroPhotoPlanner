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

# How to use the tool (in browser)

## How to setup your profile, catalogues and location:

Open ```http://127.0.0.1:8000/AstroPhotoPlanner/``` (or ```localhost:8000/AstroPhotoPlanner/```) address in your browser. Click on Register button and choose name and password.

Then ho to ```My catalogues``` and either clock on ```Import Public Catalogue``` (if you want to import one of the default catalogues such as Messier or Caldwell),
or click ```Add New Catalogue``` to add your own catalogue (you can either add objects manually one by one, or import catalogue from CSV file).

After adding the catalogues you want, go to ```My locations```, click ```Add New Location``` and add the name and GPS coordinates of the location from which you want to shoot/observe.

## Planning observations/astro-photography

Click on ```Plan observation```. Select the locaton from which you want to observe, select the catalogues with the object you want to observe and the date of observation, then click on ```Plan``` button.
You will be redirected to the table with the objects from the catalogue and you will see the time when the object is high enough in the night sky (during the night).

## Customization:

In ```My profile``` you can customize a few things. You can set minimal angle for Sun below the horizon, which will be considered as "astronomical night" (18 degrees by default).
You can also set minimal angular altitude of objects to be considered as "high enough for observation/photography" (30 degrees by default).
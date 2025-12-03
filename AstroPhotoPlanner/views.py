from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from AstroPhotoPlanner.models import UserProfile
from AstroPhotoPlanner.modules import import_from_csv
from AstroPhotoPlanner.modules.common_data_structures import GPSCoordinate
from AstroPhotoPlanner.modules.sun_movement import get_astronomical_night_start_end_times
from AstroPhotoPlanner.modules.calculate_suitable_observation_times import calculate_suitable_observation_during_time_period, object_available_from_location


import datetime

def get_user_profile(request):
    return UserProfile.objects.first()  # Replace with actual user profile retrieval logic

def index_page(request):
    return render(request, 'AstroPhotoPlanner/index_page.html')

#####################
## User Management ##
#####################

def user_profile(request):
    user_profiles = UserProfile.objects.all()
    user_info = user_profiles[0] if user_profiles else None
    return render(request, 'AstroPhotoPlanner/user_profile.html', {'user_info': user_info})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)   # automatically log in after registration
            return redirect('/AstroPhotoPlanner/')
    else:
        form = UserCreationForm()

    return render(request, "AstroPhotoPlanner/register.html", {"form": form})

def logout_page(request):
    logout(request)
    return redirect('/AstroPhotoPlanner/')


#########################
## Location Management ##
#########################

def my_locations(request):
    users_locations = UserProfile.objects.first().locations.all()
    return render(request, 'AstroPhotoPlanner/my_locations.html', {'users_locations': users_locations})

def add_location(request):
    if request.method == "POST":
        name = request.POST.get('location-name')
        gps_lat = request.POST.get('latitude')
        gps_lon = request.POST.get('longitude')
        description = request.POST.get('description', '')

        user_profile = get_user_profile(request)
        user_profile.locations.create(
            name=name,
            gps_lat=gps_lat,
            gps_lon=gps_lon,
            description=description
        )
        return redirect('/AstroPhotoPlanner/my_locations')
    else:
        return render(request, 'AstroPhotoPlanner/add_location.html')

def delete_location(request):
    if request.method == "POST":
        location_id = request.POST.get('location_id')
        user_profile = get_user_profile(request)
        location = user_profile.locations.filter(id=location_id).first()
        default_location = user_profile.preset_location
        if default_location and default_location.id == location.id:
            user_profile.preset_location = None
            user_profile.save()
        if location:
            location.delete()
    return redirect('/AstroPhotoPlanner/my_locations')

def set_location_default(request):
    if request.method == "POST":
        location_id = request.POST.get('location_id')
        user_profile = get_user_profile(request)
        location = user_profile.locations.filter(id=location_id).first()
        if location:
            user_profile.preset_location = location
            user_profile.save()
    return redirect('/AstroPhotoPlanner/my_locations')

##########################
## Catalogue Management ##
##########################

def my_catalogues(request):
    user_profile = get_user_profile(request)
    catalogues = user_profile.catalogues.all()
    return render(request, 'AstroPhotoPlanner/my_catalogues.html', {'catalogues': catalogues, 'user_profile': user_profile})

def add_catalogue(request):
    if request.method == "POST":
        name = request.POST.get('catalogue-name')

        user_profile = get_user_profile(request)
        user_profile.catalogues.create(
            name=name
        )
        return redirect('/AstroPhotoPlanner/my_catalogues')
    else:
        return render(request, 'AstroPhotoPlanner/add_catalogue.html')

def delete_catalogue(request):
    if request.method == "POST":
        catalogue_id = request.POST.get('catalogue_id')
        user_profile = get_user_profile(request)
        catalogue = user_profile.catalogues.filter(id=catalogue_id).first()
        if catalogue:
            catalogue.delete()
    return redirect('/AstroPhotoPlanner/my_catalogues')

def manage_catalogue(request, catalogue_id):
    user_profile = get_user_profile(request)
    catalogue = user_profile.catalogues.filter(id=catalogue_id).first()
    if not catalogue:
        return redirect('/AstroPhotoPlanner/my_catalogues')

    deep_sky_objects = catalogue.objects.all()
    return render(request, 'AstroPhotoPlanner/manage_catalogue.html', {'catalogue': catalogue, 'deep_sky_objects': deep_sky_objects})

# to be reviewed
def add_deep_sky_object(request, catalogue_id):
    user_profile = get_user_profile(request)
    catalogue = user_profile.catalogues.filter(id=catalogue_id).first()
    if not catalogue:
        return redirect('/AstroPhotoPlanner/my_catalogues')

    if request.method == "POST":
        name = request.POST.get('object-name')
        ra = request.POST.get('ra')
        dec = request.POST.get('dec')
        magnitude = request.POST.get('magnitude')
        object_type = request.POST.get('object-type')

        catalogue.objects.create(
            name=name,
            ra=ra,
            dec=dec,
            magnitude=magnitude,
            object_type=object_type
        )
        return redirect(f'/AstroPhotoPlanner/Manage_catalogue/{catalogue_id}')
    else:
        return render(request, 'AstroPhotoPlanner/add_deep_sky_object.html', {'catalogue': catalogue})

def edit_deep_sky_object(request, deep_sky_object_id):
    user_profile = get_user_profile(request)
    deep_sky_object = None
    for catalogue in user_profile.catalogues.all():
        deep_sky_object = catalogue.objects.filter(id=deep_sky_object_id).first()
        if deep_sky_object:
            break
    if not deep_sky_object:
        return redirect('/AstroPhotoPlanner/my_catalogues')

    if request.method == "POST":
        deep_sky_object.name = request.POST.get('object-name')
        deep_sky_object.ra = request.POST.get('ra')
        deep_sky_object.dec = request.POST.get('dec')
        deep_sky_object.magnitude = request.POST.get('magnitude')
        deep_sky_object.object_type = request.POST.get('object-type')
        deep_sky_object.plan_to_photograph = 'plan-to-photograph' in request.POST


        deep_sky_object.save()
        return redirect(f'/AstroPhotoPlanner/Manage_catalogue/{deep_sky_object.catalogue.id}')
    else:
        return render(request, 'AstroPhotoPlanner/edit_deep_sky_object.html', {'catalogue': deep_sky_object.catalogue, 'deep_sky_object': deep_sky_object})

# to be reviewed
def delete_deep_sky_object(request, catalogue_id):
    user_profile = get_user_profile(request)
    catalogue = user_profile.catalogues.filter(id=catalogue_id).first()
    if not catalogue:
        return redirect('/AstroPhotoPlanner/my_catalogues')

    if request.method == "POST":
        object_id = request.POST.get('object_id')
        deep_sky_object = catalogue.objects.filter(id=object_id).first()
        if deep_sky_object:
            deep_sky_object.delete()
    return redirect(f'/AstroPhotoPlanner/Manage_catalogue/{catalogue_id}')

def toggle_plan_object(request):
    if request.method == "POST":
        object_id = request.POST.get('object_id')
        user_profile = get_user_profile(request)
        deep_sky_object = None
        for catalogue in user_profile.catalogues.all():
            deep_sky_object = catalogue.objects.filter(id=object_id).first()
            if deep_sky_object:
                break
        if deep_sky_object:
            deep_sky_object.plan_to_photograph = not deep_sky_object.plan_to_photograph
            deep_sky_object.save()
            return redirect(f'/AstroPhotoPlanner/Manage_catalogue/{deep_sky_object.catalogue.id}')
    return redirect('/AstroPhotoPlanner/my_catalogues')

def import_catalogue_from_csv(request, catalogue_id):
    user_profile = get_user_profile(request)
    catalogue = user_profile.catalogues.filter(id=catalogue_id).first()
    print("Request:", request)
    print("FILES:", request.FILES)
    if not catalogue:
        return redirect('/AstroPhotoPlanner/my_catalogues')

    if request.method == "POST":
        csv_file = request.FILES.get('csv-file')
        print("type(csv_file): ", type(csv_file))
        if not csv_file.name.endswith('.csv'):
            return render(request, 'AstroPhotoPlanner/import_catalogue_from_csv.html', {'catalogue': catalogue, 'error': 'Please upload a valid CSV file.'})
        try:
            import_from_csv.import_catalogue_from_csv(catalogue, csv_file)
            return redirect(f'/AstroPhotoPlanner/Manage_catalogue/{catalogue_id}')
        except ValueError as e:
            return render(request, 'AstroPhotoPlanner/import_catalogue_from_csv_error.html', {'catalogue': catalogue, 'error': str(e)})
    else:
        return render(request, 'AstroPhotoPlanner/import_catalogue_from_csv.html', {'catalogue': catalogue})

###########################
## Planning observations ##
###########################

def plan_observation(request):
    user_profile = get_user_profile(request)
    locations = user_profile.locations.all()
    catalogues = user_profile.catalogues.all()
    today_date = datetime.date.today()
    return render(request, 'AstroPhotoPlanner/plan_observation.html', {'locations': locations, 'catalogues': catalogues, 'user_profile': user_profile, 'today_date': today_date})

def observation(request):
    if request.method != "POST":
        return redirect('/AstroPhotoPlanner/plan_observation')
    user_profile = get_user_profile(request)
    catalogue = get_user_profile(request).catalogues.filter(id=request.POST.get('catalogue_id')).first()
    observation_date = request.POST.get('observation_date')
    location = user_profile.locations.filter(id=request.POST.get('location')).first()
    gps_coordinates = GPSCoordinate(location.gps_lat, location.gps_lon)
    night_start, night_end = get_astronomical_night_start_end_times(gps_coordinates, observation_date, abs(user_profile.astronomical_night_angle_limit))

    objects_data = []
    for deep_sky_object in catalogue.objects.filter(plan_to_photograph=True):
        observation_periods = calculate_suitable_observation_during_time_period(
            gps_coordinates,
            night_start,
            night_end,
            deep_sky_object.ra,
            deep_sky_object.dec,
            user_profile.minimal_target_angle_above_horizon
        )

        alternative_text = ""
        alternative_text_color = "black"
        if not observation_periods:
            if not object_available_from_location(location.gps_lat, deep_sky_object.dec, user_profile.minimal_target_angle_above_horizon):
                alternative_text = "Not available from current location (never)"
                alternative_text_color = "red"
            else:
                alternative_text = "Not available this night"
                alternative_text_color = "orange"

        objects_data.append({
            'name': deep_sky_object.name,
            'ra': deep_sky_object.ra,
            'dec': deep_sky_object.dec,
            'observation_periods': observation_periods,
            'alternative_text': alternative_text,
            'alternative_text_color': alternative_text_color
        })

    print("Observation planning for date:", observation_date)
    print("Night start:", night_start)
    print("Night end:", night_end)

    context = {
        'user_profile': user_profile,
        'catalogue': catalogue,
        'location': location,
        'observation_date': observation_date,
        'night_start': night_start,
        'night_end': night_end,
        'objects_data': objects_data
    }

    return render(request, 'AstroPhotoPlanner/observation.html', context)




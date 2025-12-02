from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from AstroPhotoPlanner.models import UserProfile

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

        user_profile = UserProfile.objects.first()  # Replace with actual user profile retrieval logic
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
        user_profile = UserProfile.objects.first()  # Replace with actual user profile retrieval logic
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
        user_profile = UserProfile.objects.first()  # Replace with actual user profile retrieval logic
        location = user_profile.locations.filter(id=location_id).first()
        if location:
            user_profile.preset_location = location
            user_profile.save()
    return redirect('/AstroPhotoPlanner/my_locations')

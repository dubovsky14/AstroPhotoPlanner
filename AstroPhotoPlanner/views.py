from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from AstroPhotoPlanner.models import UserProfile

# Create your views here.
def index_page(request):
    return render(request, 'AstroPhotoPlanner/index_page.html')

# Create your views here.
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
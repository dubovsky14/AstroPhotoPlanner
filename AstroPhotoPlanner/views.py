from django.shortcuts import render
from AstroPhotoPlanner.models import UserProfile

# Create your views here.
def index_page(request):
    user_profiles = UserProfile.objects.all()
    user_info = user_profiles[0] if user_profiles else None
    return render(request, 'AstroPhotoPlanner/index.html', {'user_info': user_info})
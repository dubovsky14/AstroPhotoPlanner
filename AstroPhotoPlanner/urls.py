
from django.contrib import admin
from django.urls import include, path
from AstroPhotoPlanner import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index_page),
    path('user_profile', views.user_profile),

    path('my_locations', views.my_locations),
    path('add_location', views.add_location),
    path('delete_location', views.delete_location),
    path('set_location_default', views.set_location_default),


    # Login
    #path('login/', auth_views.LoginView.as_view(template_name='AstroPhotoPlanner/login.html', redirect_authenticated_user=True), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='AstroPhotoPlanner/login.html'), name='login'),


    # Logout
    path('logout/', views.logout_page, name='logout'),

    # Register
    path('register/', views.register, name='register'),

]

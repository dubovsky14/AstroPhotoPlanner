
from django.contrib import admin
from django.urls import include, path
from AstroPhotoPlanner import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index_page),
    path('user_profile', views.user_profile),
    path('change_user_info', views.change_user_info),

    # Login, Logout, Register
    path('login/', auth_views.LoginView.as_view(template_name='AstroPhotoPlanner/login.html'), name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register, name='register'),

    # Location Management
    path('my_locations', views.my_locations),
    path('add_location', views.add_location),
    path('delete_location', views.delete_location),
    path('set_location_default', views.set_location_default),

    # Catalogue Management
    path('my_catalogues', views.my_catalogues),
    path('add_catalogue', views.add_catalogue),
    path('delete_catalogue', views.delete_catalogue),
    path('Manage_catalogue/<int:catalogue_id>', views.manage_catalogue),
    path('add_deep_sky_object/<int:catalogue_id>', views.add_deep_sky_object),
    path('edit_deep_sky_object/<int:deep_sky_object_id>', views.edit_deep_sky_object),
    path('delete_deep_sky_object/<int:catalogue_id>', views.delete_deep_sky_object),
    path('toggle_plan_object', views.toggle_plan_object),
    path('import_catalogue_from_csv/<int:catalogue_id>', views.import_catalogue_from_csv),

    # Planner
    path('plan_observation', views.plan_observation),
    path('observation', views.observation),

]

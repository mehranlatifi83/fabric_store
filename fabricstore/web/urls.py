# urls.py
from django.urls import path
from .views import index, search, user_login, password_login, user_register, user_profile, admin_settings, add_user, edit_user, delete_user, add_fabric, edit_fabric, delete_fabric
from .views import add_address, edit_address, delete_address, load_cities, load_states_and_cities, change_email_request, activate_email, change_password, resend_activation_email
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='index'),
    path('search/', search, name='search'),  # URL جستجو
    path('login/', user_login, name='user_login'),
    path('profile/', user_profile, name='user_profile'),
    path('login/password/<str:phone>/', password_login, name='password_login'),
    path('register/<str:phone>/', user_register, name='user_register'),
    path("setting/", admin_settings, name="admin_settings"),
    path("logout/", auth_views.LogoutView.as_view(), name='logout'),
    path("adduser/", add_user, name="add_user"),
    path("addfabric/", add_fabric, name="add_fabric"),
    path("edituser/<str:user_id>/", edit_user, name="edit_user"),
    path("editfabric/<str:fabric_id>/", edit_fabric, name="edit_fabric"),
    path("deleteuser/<str:user_id>/", delete_user, name="delete_user"),
    path("deletefabric/<fabric_id>/", delete_fabric, name="delete_fabric"),
    path("addaddress/", add_address, name="add_address"),
    path("editaddress/<str:address_id>/", edit_address, name="edit_address"),
    path("deleteaddress/<str:address_id>/", delete_address, name="delete_address"),
    path('ajax/load-cities/', load_cities, name='ajax_load_cities'),
    path("loadsstateandcities/", load_states_and_cities),
    path("change_email/", change_email_request, name="change_email"),
    path("activate_email/<uuid:activation_key>/", activate_email, name="email_activate"),
    path("change_password/", change_password, name="change_password"),
    path("resend_activation_email/<str:activation_id>/", resend_activation_email, name="resend_activation"),
]

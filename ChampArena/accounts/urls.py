from django.urls import path
from . import views
app_name="accounts"
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('host/<int:host_id>/', views.host_profile, name='host_profile'),

]


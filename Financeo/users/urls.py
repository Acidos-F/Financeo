from django.contrib import admin
from django.urls import path
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.login_view, name='login'),
    path('signup/', user_views.signup_view, name='signup'),
    path('dashboard/', user_views.dashboard_view, name='dashboard'),
]

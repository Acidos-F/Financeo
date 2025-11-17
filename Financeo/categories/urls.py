from django.urls import path
from . import views

urlpatterns = [
    path("", views.category_list, name="categories"),
    path("create/", views.create_category, name="create_category"),
    path("<int:category_id>/update/", views.update_category, name="update_category"),
    path("<int:category_id>/delete/", views.delete_category, name="delete_category"),
]

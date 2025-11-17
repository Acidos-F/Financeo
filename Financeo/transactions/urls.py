from django.urls import path
from . import views

urlpatterns = [
    path("", views.transaction_list, name="transactions"),
    path("create/", views.create_transaction, name="create_transaction"),
    path("<int:transaction_id>/update/", views.update_transaction, name="update_transaction"),
    path("<int:transaction_id>/delete/", views.delete_transaction, name="delete_transaction"),
    path("search/", views.search_transactions_ajax, name="search_transactions_ajax"),
]
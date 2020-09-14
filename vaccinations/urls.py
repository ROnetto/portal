from django.urls import path

from vaccinations.views import vaccination_list_create_view, vaccination_retrieve_update_delete_view

app_name = "vaccinations"
urlpatterns = [
    path('', vaccination_list_create_view, name='list_create'),
    path('/<int:id>', vaccination_retrieve_update_delete_view, name='retrieve_update_delete'),
]

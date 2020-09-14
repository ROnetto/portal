from django.urls import path

from drugs.views import drug_list_create_view, drug_retrieve_update_delete_view

app_name = "drugs"
urlpatterns = [
    path('', drug_list_create_view, name='list_create'),
    path('/<int:id>', drug_retrieve_update_delete_view, name='retrieve_update_delete'),
]

from django.urls import path
from .views import (
  lead_list, lead_detail, lead_create, lead_update, lead_delete,
  LeadListView, LeaDetailView, LeaCreateView, LeaUpdateView, LeadDeleteView,
)
app_name = "leads"

# this is actually /leads/all path becasue we are calling leads/ inside our orginal urls.py path inside djcrm app file
# Good to add name="" instead of hardcoding the url path just incase in the furtue the path changes but then the name never does

urlpatterns = [
    path('', LeadListView.as_view(), name='lead-list'),
    path('<int:pk>/', LeaDetailView.as_view(), name='lead-detail'),
    path('create/', LeaCreateView.as_view(), name='lead-create'),
    path('<int:pk>/update/', LeaUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),

    # path('', lead_list, name='lead-list'),
    # primary key - the id of the lead that is held identifies it in our sqldatabase 
    # path('create/', lead_create, name='lead-create'),
    # path('<int:pk>/', lead_detail, name='lead-detail'),
    # path('<int:pk>/delete/', lead_delete, name='lead-delete'),
    # path('<int:pk>/update/', lead_update, name='lead-update'),

]
from django.urls import path
from . import views


urlpatterns = [
    path('software-providers/', views.SoftwareProviderListView.as_view(), name='software_providers_list'),
    path('licences/', views.LicenceListView.as_view(), name='licences_list'),
]

from rest_framework.viewsets import ModelViewSet
from netbox_licences.models import Licence, Software
from .serializers import SoftwareSerializer, LicenceSerializer
from netbox_licences.filters import SoftwareFilter

class SoftwareViewSet(ModelViewSet):
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer
    filterset_class = SoftwareFilter

class LicenceViewSet(ModelViewSet):
    queryset = Licence.objects.all()
    serializer_class = LicenceSerializer


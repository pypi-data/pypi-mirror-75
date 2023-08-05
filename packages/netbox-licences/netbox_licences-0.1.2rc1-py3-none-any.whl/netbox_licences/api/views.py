from rest_framework.viewsets import ModelViewSet
from netbox_licences.models import Licence, Software
from .serializers import SoftwareSerializer, LicenceSerializer

class SoftwareViewSet(ModelViewSet):
    queryset = Software.objects.all()
    serializer_class = Software

class LicenceViewSet(ModelViewSet):
    queryset = Licence.objects.all()
    serializer_class = Licence


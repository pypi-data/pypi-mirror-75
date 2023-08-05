from rest_framework.serializers import ModelSerializer
from netbox_licences.models import Licence, Software
import sys

sys.exit()

class SoftwareSerializer(ModelSerializer):
    class Meta:
        model = Software
        fields = ('id', 'name', 'provider', 'softtype')


class LicenceSerializer(ModelSerializer):
    class Meta:
        model = Licence
        fields = ('id', 'inventory_number', 'licencetype', 'date_created', 'date_valid', 'amount', 'software', 'tenant')

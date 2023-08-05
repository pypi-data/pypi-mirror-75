import django_tables2 as tables
from utilities.tables import BaseTable, ToggleColumn

from .models import SoftwareProvider, Licence

class SoftwareProviderTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = SoftwareProvider
        fields = (
            "name",
            "full_name"
        )

class LicenceTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = Licence
        fields = (
            "inventory_number",
            "licencetype",
            "date_created",
            "date_valid",
            "amount",
            "software",
            "tenant",
            "site"
        )

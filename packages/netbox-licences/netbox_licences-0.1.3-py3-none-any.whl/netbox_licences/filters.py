import django_filters
from django.db.models import Q

from dcim.models import Site

from utilities.filters import (
   BaseFilterSet,
   MultiValueCharFilter,
   MultiValueMACAddressFilter,
   MultiValueNumberFilter,
   NameSlugSearchFilterSet,
   TagFilter,
   TreeNodeMultipleChoiceFilter,
)

from extras.filters import CustomFieldFilterSet, LocalConfigContextFilterSet, CreatedUpdatedFilterSet

from .models import SoftwareProvider, Software, Licence


class CommonLicencesFilter(BaseFilterSet):
    q = django_filters.CharFilter(method="search", label="Search")

    class Meta:
        model = SoftwareProvider
        fields = ["id", "name"]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(id__icontains=value)
            | Q(name__icontains=value)
        )
        return queryset.filter(qs_filter)




class SoftwareFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(method="search", label="Search")

    class Meta:
        model = Software
        fields = [
            "id",
            "name",
            "provider",
            "softtype",
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(id__icontains=value)
            | Q(name__icontains=value)
        )
        return queryset.filter(qs_filter)




class LicencesFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(method="search", label="Search")

    software = django_filters.ModelMultipleChoiceFilter(
        queryset = Software.objects.all(),
        # field_name = 'software__id',
        # lookup_expr='in',
        # to_field_name='id', # CANNOT resolve into field
        label = "Software"
    )

    site_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        label = "Site"
    )

    # Use it when need children data
    # site = django_filters.ModelMultipleChoiceFilter(
    #     queryset = Site.objects.all(),
    #     field_name = 'site__slug',
    #     lookup_expr='in',
    #     to_field_name='slug',
    #     label = "Site"
    # )

    class Meta:
        model = Licence
        fields = [
            "id",
            "inventory_number",
            "date_created",
            "date_valid",
            "amount",
            "software",
            "site",
            "tenant"
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(id__icontains=value)
            | Q(inventory_number__icontains=value)
        )
        return queryset.filter(qs_filter)

    def search_in_field(self, search, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            search
        )
        return queryset.filter(qs_filter)

    def search_inv_num(self, queryset, name, value):
        return self.search_in_field(Q(inventory_number__icontains=value), queryset, name, value)

    def search_software(self, queryset, name, value):
        return self.search_in_field(Q(software__icontains=value), queryset, name, value)

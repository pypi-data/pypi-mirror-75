from django import forms
from django_rq import get_queue

from .models import SoftwareProvider, Licence, Software

from mptt.forms import TreeNodeChoiceField

from utilities.forms import (
    APISelectMultiple,
    DynamicModelMultipleChoiceField,
    StaticSelect2Multiple,
    BootstrapMixin
)

from dcim.models import Site


class CommonLicencesFilterForm(BootstrapMixin, forms.ModelForm):

    q = forms.CharField(required=False, label="Search")

    class Meta:
        model = SoftwareProvider
        fields = [
            "q",
        ]

class LicencesFilterForm(BootstrapMixin, forms.ModelForm):
    q = forms.CharField(required=False, label="Search")

    inventory_number = forms.CharField(required=False, label="Inventory Number")

    # software = DynamicModelMultipleChoiceField(
    #     queryset=Software.objects.all(),
    #     required=False,
    #     to_field_name="software__slug",
    #     widget=APISelectMultiple(
    #         value_field="software__slug",
    #     )
    # )

    site = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        to_field_name="site__slug",
         widget=APISelectMultiple(
            value_field="site__slug",
        )
    )

    class Meta:
        model = Licence
        fields = [
            "q",
            "inventory_number",
            "site",
            # "software"
        ]

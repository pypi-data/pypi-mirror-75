from django.db import models

class NamedModel(models.Model):
    """ Base for the most models """
    name = models.CharField(max_length=50)

    class Meta:
        ordering = [ 'name' ]
        abstract = True

    def __str__(self):
        return self.name

class SoftwareProvider(NamedModel):
    full_name = models.CharField(max_length=64)


class SoftwareType(NamedModel): pass

class Software(NamedModel):
    provider = models.ForeignKey(on_delete=models.deletion.CASCADE,to='SoftwareProvider')
    softtype = models.ForeignKey(on_delete=models.deletion.CASCADE,to='SoftwareType')

class LicenceType(NamedModel): pass

class Licence(models.Model):
    inventory_number =  models.CharField(unique=True, max_length=50)
    licencetype =  models.ForeignKey(null=True,on_delete=models.deletion.CASCADE,to='LicenceType')
    date_created =  models.DateTimeField(auto_now=True)
    date_valid =  models.DateField()
    amount = models.IntegerField()
    software = models.ForeignKey(blank=True, null=True,on_delete=models.deletion.CASCADE,to='Software')
    tenant =  models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE,to='tenancy.Tenant')
    site =  models.ForeignKey(blank=True, null=True,on_delete=models.deletion.CASCADE,to='dcim.Site')


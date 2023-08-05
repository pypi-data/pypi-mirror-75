from django.db import migrations,models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tenancy', '0003_unicode_literals')
    ]

    operations = [
        migrations.CreateModel(
            name='SoftwareProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=50)),
            ],
            options = {
                'ordering': ['name']
            }
        ),
        migrations.CreateModel(
            name='SoftwareType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
            options = {
                'ordering': ['name']
            }
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('provider', models.ForeignKey(on_delete=models.deletion.CASCADE,to='SoftwareProvider')),
                ('softtype', models.ForeignKey(on_delete=models.deletion.CASCADE,to='SoftwareType')),
            ],
            options = {
                 'ordering': ['name']
            },
        ),
        migrations.CreateModel(
            name='LicenceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
            options = {
                'ordering': ['name']
            }
        ),
        migrations.CreateModel(
            name='Licence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('inventory_number', models.CharField(unique=True, max_length=50)),
                ('licencetype', models.ForeignKey(null=True,on_delete=models.deletion.CASCADE,to='LicenceType')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_valid', models.DateField()),
                ('amount', models.IntegerField()),
                ('software', models.ForeignKey(blank=True, null=True,on_delete=models.deletion.CASCADE,to='Software')),
                ('tenant', models.ForeignKey(blank=True, null=True,on_delete=models.deletion.CASCADE,to='tenancy.Tenant')),
                ('site', models.ForeignKey(blank=True, null=True,on_delete=models.deletion.CASCADE,to='dcim.Site')),
            ],
            options = {
                'ordering': ['name']
            }
        ),
        # migrations.CreateModel(
        #     name='SoftwareSupport',
        #     fields=[
        #         ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
        #         ('')
        #     ]
        # ),
        # migrations.CreateModel(
        #     name='HardwareSupport',
        #     fields=[
        #         ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
        #         ('')
        #     ]
        # ),
    ]

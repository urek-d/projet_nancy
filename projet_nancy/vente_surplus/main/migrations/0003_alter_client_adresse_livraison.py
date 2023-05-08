# Generated by Django 4.2 on 2023-04-11 02:35

import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_lieu_nom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='adresse_livraison',
            field=django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(0.0, 0.0), geography=True, srid=4326),
        ),
    ]

# Generated by Django 5.0.3 on 2024-03-10 00:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akevision_rest', '0005_remove_client_security_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='compagnie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='akevision_rest.compagnie'),
        ),
    ]

# Generated by Django 5.0.3 on 2024-03-14 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('akevision_rest', '0013_accesstoken_refreshtoken_remove_client_token_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='client',
            unique_together={('name', 'compagnie')},
        ),
    ]

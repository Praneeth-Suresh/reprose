# Generated by Django 4.2.5 on 2023-09-07 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookapp', '0006_listings_times_viewed'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='borrowed_date',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
    ]

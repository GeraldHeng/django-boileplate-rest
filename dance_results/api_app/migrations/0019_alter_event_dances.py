# Generated by Django 3.2.6 on 2021-08-16 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0018_auto_20210814_0434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='dances',
            field=models.ManyToManyField(related_name='events', to='api_app.Dance'),
        ),
    ]

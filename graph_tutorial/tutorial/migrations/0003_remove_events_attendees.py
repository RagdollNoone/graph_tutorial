# Generated by Django 2.1.3 on 2019-08-06 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0002_attendees'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='Attendees',
        ),
    ]

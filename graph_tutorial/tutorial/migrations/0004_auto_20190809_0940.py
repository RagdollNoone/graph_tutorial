# Generated by Django 2.1.3 on 2019-08-09 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0003_remove_events_attendees'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('Id', models.IntegerField(primary_key=True, serialize=False)),
                ('Openid', models.CharField(max_length=255)),
                ('Address', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.AddField(
            model_name='attendees',
            name='Attendtime',
            field=models.DateTimeField(default=''),
        ),
        migrations.AddField(
            model_name='attendees',
            name='Isattend',
            field=models.IntegerField(default='0'),
        ),
        migrations.AddField(
            model_name='attendees',
            name='Meetingtime',
            field=models.DateTimeField(default=''),
        ),
    ]

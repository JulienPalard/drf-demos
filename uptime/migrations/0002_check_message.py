# Generated by Django 3.2 on 2021-04-24 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uptime', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
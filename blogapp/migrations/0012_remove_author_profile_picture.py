# Generated by Django 2.0 on 2017-12-20 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0011_author_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='profile_picture',
        ),
    ]
# Generated by Django 3.2 on 2022-05-26 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('receipt', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='check',
            old_name='check_type',
            new_name='type',
        ),
    ]
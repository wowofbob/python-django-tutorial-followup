# Generated by Django 3.0.3 on 2020-02-28 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_somemodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='somemodel',
            name='some_another_text',
        ),
    ]

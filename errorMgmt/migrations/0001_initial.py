# Generated by Django 3.2.6 on 2021-10-20 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ResponseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('error', models.CharField(max_length=128)),
                ('status', models.IntegerField()),
                ('entry_date', models.DateTimeField()),
            ],
        ),
    ]

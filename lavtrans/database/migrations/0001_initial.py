# Generated by Django 4.1.5 on 2023-01-16 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10)),
                ('tehosmotr', models.DateField()),
                ('strahovka', models.DateField()),
                ('tamogennoye', models.DateField()),
                ('tahograf', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('passport', models.DateField()),
                ('visa', models.DateField()),
                ('driver_card', models.DateField()),
            ],
        ),
    ]

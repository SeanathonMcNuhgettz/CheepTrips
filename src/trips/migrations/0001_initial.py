# Generated by Django 3.0.5 on 2020-05-11 01:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_carrier', models.CharField(max_length=200)),
                ('departure_time', models.DateTimeField(verbose_name='Departure date')),
                ('arrival_time', models.DateTimeField(verbose_name='Arrival date')),
                ('num_passengers', models.IntegerField(default=1)),
                ('num_bags', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('budget', models.IntegerField(default=0)),
                ('cost', models.IntegerField(default=0)),
                ('flights', models.ManyToManyField(to='trips.Flight')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exchange_rate', models.IntegerField(default=1)),
                ('cost_of_living', models.IntegerField(default=0)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.Region')),
            ],
        ),
        migrations.AddField(
            model_name='flight',
            name='departure_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departures', to='trips.Location'),
        ),
        migrations.AddField(
            model_name='flight',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrivals', to='trips.Location'),
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('locations', models.ManyToManyField(to='trips.Location')),
            ],
        ),
    ]

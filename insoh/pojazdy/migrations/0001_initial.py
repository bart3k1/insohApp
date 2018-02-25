# Generated by Django 2.0.2 on 2018-02-24 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Baterie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=50, null=True)),
                ('numer', models.IntegerField(null=True)),
                ('batID', models.IntegerField(null=True)),
                ('on', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pojazdy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.CharField(max_length=64, unique=True)),
                ('nazwa', models.CharField(max_length=50)),
                ('bateries', models.ManyToManyField(to='pojazdy.Baterie')),
            ],
        ),
    ]

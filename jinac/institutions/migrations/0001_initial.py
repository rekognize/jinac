# Generated by Django 2.1.5 on 2019-02-06 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('short_name', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'verbose_name': 'institution',
                'verbose_name_plural': 'institutions',
            },
        ),
    ]

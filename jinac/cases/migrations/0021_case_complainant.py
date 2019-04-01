# Generated by Django 2.1.5 on 2019-03-30 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0026_complainant'),
        ('cases', '0020_trialdecision'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='complainant',
            field=models.ManyToManyField(blank=True, to='people.Complainant', verbose_name='complainant'),
        ),
    ]
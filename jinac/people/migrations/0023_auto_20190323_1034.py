# Generated by Django 2.1.5 on 2019-03-23 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0022_auto_20190323_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journaliststatus',
            name='prison',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jurisdiction.Prison', verbose_name='prison'),
        ),
    ]

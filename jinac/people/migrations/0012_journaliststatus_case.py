# Generated by Django 2.1.5 on 2019-03-05 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0003_auto_20190305_0617'),
        ('people', '0011_auto_20190304_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='journaliststatus',
            name='case',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cases.Case', verbose_name='case'),
        ),
    ]

# Generated by Django 2.1.5 on 2019-07-08 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jurisdiction', '0006_auto_20190418_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='prison',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jurisdiction.City', verbose_name='city'),
        ),
    ]

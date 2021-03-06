# Generated by Django 2.1.5 on 2019-03-29 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jurisdiction', '0004_auto_20190309_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='court',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jurisdiction.City', verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='prison',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='name'),
        ),
    ]

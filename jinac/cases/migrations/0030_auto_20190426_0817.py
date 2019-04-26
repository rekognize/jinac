# Generated by Django 2.1.5 on 2019-04-26 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0029_auto_20190425_2052'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='case',
            options={'ordering': ('order', '-modified'), 'verbose_name': 'case', 'verbose_name_plural': 'cases'},
        ),
        migrations.AddField(
            model_name='case',
            name='order',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
# Generated by Django 2.1.5 on 2019-10-01 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infographics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infographic',
            name='embed_code',
            field=models.TextField(blank=True, null=True, verbose_name='embed code'),
        ),
    ]

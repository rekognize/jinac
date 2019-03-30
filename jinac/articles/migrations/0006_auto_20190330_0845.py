# Generated by Django 2.1.5 on 2019-03-30 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_article_about_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='lang',
            field=models.CharField(choices=[('tr', 'Turkish'), ('en', 'English')], max_length=5, verbose_name='language'),
        ),
    ]

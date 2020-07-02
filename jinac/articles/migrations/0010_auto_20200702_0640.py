# Generated by Django 2.1.5 on 2020-07-02 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0009_auto_20190614_0837'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ('-added',), 'verbose_name': 'article', 'verbose_name_plural': 'articles'},
        ),
        migrations.AddField(
            model_name='article',
            name='translation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='articles.Article', verbose_name='translation'),
        ),
    ]

# Generated by Django 2.1.5 on 2019-03-30 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0025_auto_20190323_1108'),
        ('cases', '0019_auto_20190330_0845'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrialDecision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decision_type', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'acquittal'), (1, 'fine'), (2, 'imprisonment'), (6, 'postponed'), (7, 'judgement receded')], null=True, verbose_name='decision type')),
                ('punishment_year', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='year')),
                ('punishment_month', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='month')),
                ('punishment_day', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='day')),
                ('punishment_fine', models.CharField(blank=True, max_length=100, null=True, verbose_name='fine')),
                ('articles', models.ManyToManyField(blank=True, to='cases.Article', verbose_name='articles')),
                ('journalist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.Journalist', verbose_name='journalists')),
                ('trial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Trial', verbose_name='trial')),
            ],
            options={
                'verbose_name': 'trial - decision relation',
                'verbose_name_plural': 'trial - decision relations',
            },
        ),
    ]
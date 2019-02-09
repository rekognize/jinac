# Generated by Django 2.1.5 on 2019-02-07 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_plaintiff'),
        ('cases', '0004_trial_next_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='decision',
            name='journalists',
        ),
        migrations.RemoveField(
            model_name='decision',
            name='trial',
        ),
        migrations.RemoveField(
            model_name='indictment',
            name='requested_punishment_amount',
        ),
        migrations.RemoveField(
            model_name='indictment',
            name='requested_punishment_type',
        ),
        migrations.AddField(
            model_name='case',
            name='plaintiff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='people.Plaintiff', verbose_name='plaintiff'),
        ),
        migrations.AddField(
            model_name='casejournalist',
            name='punishment_amount',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='punishment amount'),
        ),
        migrations.AddField(
            model_name='casejournalist',
            name='punishment_type',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'imprisonment'), (2, 'fine')], null=True, verbose_name='punishment type'),
        ),
        migrations.DeleteModel(
            name='Decision',
        ),
    ]
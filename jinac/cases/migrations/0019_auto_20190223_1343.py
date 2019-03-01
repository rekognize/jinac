# Generated by Django 2.1.5 on 2019-02-23 13:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0018_auto_20190223_1209'),
    ]

    operations = [
        migrations.RenameField(
            model_name='caseindictment',
            old_name='indictmen',
            new_name='indictment',
        ),
        migrations.RemoveField(
            model_name='trial',
            name='time',
        ),
        migrations.RemoveField(
            model_name='trialdocumenttype',
            name='description',
        ),
        migrations.RemoveField(
            model_name='trialdocumenttype',
            name='file',
        ),
        migrations.AddField(
            model_name='article',
            name='punishment_amount_max',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='maximum punishment due'),
        ),
        migrations.AddField(
            model_name='article',
            name='punishment_amount_min',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='minimum punishment due'),
        ),
        migrations.AddField(
            model_name='article',
            name='punishment_type',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'fine'), (2, 'imprisonment')], null=True, verbose_name='punishment type'),
        ),
        migrations.AddField(
            model_name='casedocument',
            name='publish',
            field=models.BooleanField(default=True, verbose_name='publish'),
        ),
        migrations.AddField(
            model_name='notetype',
            name='publish',
            field=models.BooleanField(default=True, verbose_name='publish'),
        ),
        migrations.AddField(
            model_name='trial',
            name='time_announced',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='announced time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trial',
            name='time_start',
            field=models.DateTimeField(blank=True, null=True, verbose_name='start time'),
        ),
        migrations.AddField(
            model_name='trialdocumenttype',
            name='type',
            field=models.CharField(default='x', max_length=50, verbose_name='type'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='case',
            name='coup_related',
            field=models.BooleanField(default=False, verbose_name='coup attempt related'),
        ),
        migrations.AlterField(
            model_name='case',
            name='judge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='people.Judge', verbose_name='presiding judge'),
        ),
        migrations.AlterField(
            model_name='casejournalist',
            name='decision_type',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'acquittal'), (1, 'fine'), (2, 'imprisonment')], null=True, verbose_name='decision type'),
        ),
    ]
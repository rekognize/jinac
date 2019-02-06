# Generated by Django 2.1.5 on 2019-02-04 12:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(verbose_name='note')),
            ],
            options={
                'verbose_name': 'note',
                'verbose_name_plural': 'notes',
            },
        ),
        migrations.RemoveField(
            model_name='witness',
            name='type',
        ),
        migrations.AlterModelOptions(
            name='case',
            options={'verbose_name': 'case', 'verbose_name_plural': 'case'},
        ),
        migrations.AlterModelOptions(
            name='decision',
            options={'verbose_name': 'decision', 'verbose_name_plural': 'decisions'},
        ),
        migrations.AlterModelOptions(
            name='indictment',
            options={'verbose_name': 'indictment', 'verbose_name_plural': 'indictments'},
        ),
        migrations.AlterModelOptions(
            name='trial',
            options={'verbose_name': 'trial', 'verbose_name_plural': 'trials'},
        ),
        migrations.AlterModelOptions(
            name='trialdocument',
            options={'verbose_name': 'trial document', 'verbose_name_plural': 'trial documents'},
        ),
        migrations.AlterModelOptions(
            name='trialdocumenttype',
            options={'verbose_name': 'trial document type', 'verbose_name_plural': 'trial document types'},
        ),
        migrations.AlterModelOptions(
            name='trialviolation',
            options={'verbose_name': 'right violation', 'verbose_name_plural': 'right violations'},
        ),
        migrations.RemoveField(
            model_name='trial',
            name='witnesses',
        ),
        migrations.AlterField(
            model_name='case',
            name='added',
            field=models.DateTimeField(auto_now_add=True, verbose_name='added time'),
        ),
        migrations.AlterField(
            model_name='case',
            name='court',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jurisdiction.Court', verbose_name='court'),
        ),
        migrations.AlterField(
            model_name='case',
            name='name',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='case',
            name='no',
            field=models.CharField(max_length=20, verbose_name='number'),
        ),
        migrations.AlterField(
            model_name='case',
            name='parent_case',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cases.Case', verbose_name='parent case'),
        ),
        migrations.AlterField(
            model_name='case',
            name='reporter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='reporter'),
        ),
        migrations.AlterField(
            model_name='case',
            name='start_date',
            field=models.DateField(verbose_name='start date'),
        ),
        migrations.AlterField(
            model_name='decision',
            name='date',
            field=models.DateField(verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='decision',
            name='is_final',
            field=models.BooleanField(default=False, verbose_name='is final decision'),
        ),
        migrations.AlterField(
            model_name='decision',
            name='journalists',
            field=models.ManyToManyField(blank=True, to='journalists.Journalist', verbose_name='journalists'),
        ),
        migrations.AlterField(
            model_name='decision',
            name='punishment_amount',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='punishment amount'),
        ),
        migrations.AlterField(
            model_name='decision',
            name='punishment_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jurisdiction.PunishmentType', verbose_name='punishment type'),
        ),
        migrations.AlterField(
            model_name='decision',
            name='trial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Trial', verbose_name='trial'),
        ),
        migrations.AlterField(
            model_name='decision',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jurisdiction.DecisionType', verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='indictment',
            name='case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Case', verbose_name='case'),
        ),
        migrations.AlterField(
            model_name='indictment',
            name='date',
            field=models.DateField(verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='indictment',
            name='journalists',
            field=models.ManyToManyField(blank=True, to='journalists.Journalist', verbose_name='journalists'),
        ),
        migrations.AlterField(
            model_name='indictment',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jurisdiction.IndictmentType', verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='trial',
            name='added',
            field=models.DateTimeField(auto_now_add=True, verbose_name='added time'),
        ),
        migrations.AlterField(
            model_name='trial',
            name='attorneys',
            field=models.ManyToManyField(blank=True, to='jurisdiction.Attorney', verbose_name='attorney'),
        ),
        migrations.AlterField(
            model_name='trial',
            name='board',
            field=models.ManyToManyField(blank=True, related_name='board_memberships', to='jurisdiction.Judge', verbose_name='board of judges'),
        ),
        migrations.AlterField(
            model_name='trial',
            name='case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Case', verbose_name='case'),
        ),
        migrations.AlterField(
            model_name='trial',
            name='defendant_count',
            field=models.PositiveIntegerField(verbose_name='defendant count'),
        ),
        migrations.AlterField(
            model_name='trial',
            name='journalist_count',
            field=models.PositiveIntegerField(verbose_name='journalist count'),
        ),
        migrations.AlterField(
            model_name='trial',
            name='judge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jurisdiction.Judge', verbose_name='judge'),
        ),
        migrations.AlterField(
            model_name='trial',
            name='observers',
            field=models.ManyToManyField(blank=True, to='journalists.Institution', verbose_name='institutional observers'),
        ),
        migrations.AlterField(
            model_name='trial',
            name='prosecutor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jurisdiction.Prosecutor', verbose_name='prosecutor'),
        ),
        migrations.AlterField(
            model_name='trial',
            name='reporter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='reporter'),
        ),
        migrations.AlterField(
            model_name='trial',
            name='session_no',
            field=models.PositiveIntegerField(verbose_name='session'),
        ),
        migrations.AlterField(
            model_name='trial',
            name='summary',
            field=models.TextField(blank=True, null=True, verbose_name='summary'),
        ),
        migrations.AlterField(
            model_name='trial',
            name='time',
            field=models.DateTimeField(verbose_name='time'),
        ),
        migrations.AlterField(
            model_name='trial',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jurisdiction.TrialType', verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='trialdocument',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='trialdocument',
            name='file',
            field=models.FileField(upload_to='', verbose_name='file'),
        ),
        migrations.AlterField(
            model_name='trialdocument',
            name='trial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Trial', verbose_name='trial'),
        ),
        migrations.AlterField(
            model_name='trialdocument',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cases.TrialDocumentType', verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='trialdocumenttype',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='trialdocumenttype',
            name='file',
            field=models.FileField(upload_to='', verbose_name='file'),
        ),
        migrations.AlterField(
            model_name='trialviolation',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='trialviolation',
            name='trial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Trial', verbose_name='trial'),
        ),
        migrations.AlterField(
            model_name='trialviolation',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jurisdiction.ViolationType', verbose_name='violation type'),
        ),
        migrations.DeleteModel(
            name='Witness',
        ),
        migrations.DeleteModel(
            name='WitnessType',
        ),
    ]

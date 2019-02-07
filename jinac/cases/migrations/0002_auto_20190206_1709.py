# Generated by Django 2.1.5 on 2019-02-06 17:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cases', '0001_initial'),
        ('people', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institutions', '0001_initial'),
        ('jurisdiction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='decision',
            name='journalists',
            field=models.ManyToManyField(blank=True, to='people.Journalist', verbose_name='journalists'),
        ),
        migrations.AddField(
            model_name='decision',
            name='trial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Trial', verbose_name='trial'),
        ),
        migrations.AddField(
            model_name='casenote',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cases.NoteType', verbose_name='type'),
        ),
        migrations.AddField(
            model_name='casejournalist',
            name='case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Case', verbose_name='case'),
        ),
        migrations.AddField(
            model_name='casejournalist',
            name='institution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institutions.Institution', verbose_name='institution'),
        ),
        migrations.AddField(
            model_name='casejournalist',
            name='journalist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.Journalist', verbose_name='journalists'),
        ),
        migrations.AddField(
            model_name='casedocument',
            name='case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Case', verbose_name='case'),
        ),
        migrations.AddField(
            model_name='casedocument',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cases.CaseDocumentType', verbose_name='type'),
        ),
        migrations.AddField(
            model_name='case',
            name='board',
            field=models.ManyToManyField(blank=True, related_name='board_memberships', to='people.Judge', verbose_name='board of judges'),
        ),
        migrations.AddField(
            model_name='case',
            name='court',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jurisdiction.Court', verbose_name='court'),
        ),
        migrations.AddField(
            model_name='case',
            name='defendant_attorneys',
            field=models.ManyToManyField(blank=True, to='people.Attorney', verbose_name='defendant attorneys'),
        ),
        migrations.AddField(
            model_name='case',
            name='journalists',
            field=models.ManyToManyField(through='cases.CaseJournalist', to='people.Journalist'),
        ),
        migrations.AddField(
            model_name='case',
            name='judge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='people.Judge', verbose_name='judge'),
        ),
        migrations.AddField(
            model_name='case',
            name='parent_case',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cases.Case', verbose_name='parent case'),
        ),
        migrations.AddField(
            model_name='case',
            name='prosecutor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='people.Prosecutor', verbose_name='prosecutor'),
        ),
        migrations.AddField(
            model_name='case',
            name='reporter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='reporter'),
        ),
        migrations.AddField(
            model_name='case',
            name='scope',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cases.CaseScope', verbose_name='case scope'),
        ),
    ]

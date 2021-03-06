# Generated by Django 2.1.5 on 2019-03-08 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0012_journaliststatus_case'),
    ]

    operations = [
        migrations.CreateModel(
            name='JournalistNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(verbose_name='note')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('journalist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.Journalist', verbose_name='journalist')),
            ],
            options={
                'verbose_name': 'case note',
                'verbose_name_plural': 'case notes',
            },
        ),
        migrations.CreateModel(
            name='JournalistNoteType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100, verbose_name='type')),
                ('publish', models.BooleanField(default=True, verbose_name='publish')),
            ],
            options={
                'verbose_name': 'case note type',
                'verbose_name_plural': 'case note types',
            },
        ),
        migrations.AddField(
            model_name='journalistnote',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='people.JournalistNoteType', verbose_name='type'),
        ),
    ]

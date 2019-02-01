# Generated by Django 2.1.5 on 2019-02-01 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('short_name', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Journalist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(blank=True, choices=[('m', 'male'), ('f', 'female')], max_length=2, null=True)),
                ('has_press_card', models.NullBooleanField(default=None)),
                ('birth_year', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JournalistInstitution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started', models.DateField(blank=True, null=True)),
                ('ended', models.DateField(blank=True, null=True)),
                ('ongoing', models.BooleanField(default=True)),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='journalists.Institution')),
                ('journalist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journalists.Journalist')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField()),
                ('date_end', models.DateField(blank=True, null=True)),
                ('journalist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journalists.Journalist')),
            ],
        ),
        migrations.CreateModel(
            name='WorkPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='journalistinstitution',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='journalists.WorkPosition'),
        ),
        migrations.AddField(
            model_name='journalist',
            name='institutions',
            field=models.ManyToManyField(blank=True, through='journalists.JournalistInstitution', to='journalists.Institution', verbose_name='Institutions'),
        ),
    ]

# Generated by Django 3.0.3 on 2020-02-29 10:45

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('booi_operations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=2055)),
                ('answer', models.TextField()),
                ('add_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-add_time'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to', models.CharField(choices=[('for_all', 'for_all'), ('new_commer', 'new_commer')], max_length=255)),
                ('noti_type', models.CharField(choices=[('new book', 'new book'), ('text', 'text')], max_length=255)),
                ('noti_body', tinymce.models.HTMLField(blank=True, null=True)),
                ('read', models.BooleanField(default=False)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='ReportToBookOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=55)),
                ('message', models.TextField()),
                ('subject', models.CharField(max_length=555)),
                ('solution', models.TextField(null=True)),
            ],
            options={
                'ordering': ['-report_time'],
            },
        ),
        migrations.CreateModel(
            name='ReportToBorrower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('working on it', 'working on it'), ('solved', 'solved')], max_length=55)),
                ('message', models.TextField()),
                ('solution', models.TextField(null=True)),
                ('subject', models.CharField(max_length=555)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booi_operations.Booi')),
            ],
            options={
                'ordering': ['-report_time'],
            },
        ),
    ]

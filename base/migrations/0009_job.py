# Generated by Django 5.0.7 on 2024-07-12 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_request_date_updated_alter_request_file_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sector', models.CharField(max_length=50)),
                ('company_name', models.CharField(max_length=255)),
                ('job_title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('verified', models.BooleanField(default=False)),
            ],
        ),
    ]

# Generated by Django 5.0.7 on 2024-07-10 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alumni_avatar_alumni_proof'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumni',
            name='student_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]

# Generated by Django 5.0.6 on 2024-08-03 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentic', '0002_alter_customuser_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]

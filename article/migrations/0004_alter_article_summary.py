# Generated by Django 5.0.6 on 2024-05-23 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_alter_article_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='summary',
            field=models.CharField(max_length=200),
        ),
    ]

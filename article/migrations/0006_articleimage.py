# Generated by Django 5.0.6 on 2024-06-04 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_alter_article_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
            ],
        ),
    ]

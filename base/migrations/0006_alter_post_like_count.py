# Generated by Django 3.2.9 on 2022-04-06 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_post_like_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='like_count',
            field=models.IntegerField(default=0),
        ),
    ]
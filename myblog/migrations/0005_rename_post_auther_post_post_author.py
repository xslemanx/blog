# Generated by Django 4.2.4 on 2023-08-28 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0004_alter_post_post_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='post_auther',
            new_name='post_author',
        ),
    ]
# Generated by Django 5.0.6 on 2024-05-29 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="BlogPost",
            new_name="Post",
        ),
    ]

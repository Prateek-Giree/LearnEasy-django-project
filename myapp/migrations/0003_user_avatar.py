# Generated by Django 5.0.6 on 2024-06-22 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_user_bio_user_name_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatar.png', null=True, upload_to=''),
        ),
    ]

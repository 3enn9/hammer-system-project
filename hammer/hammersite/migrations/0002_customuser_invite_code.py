# Generated by Django 5.1.3 on 2024-11-30 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hammersite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='invite_code',
            field=models.CharField(default=1234, max_length=6),
            preserve_default=False,
        ),
    ]
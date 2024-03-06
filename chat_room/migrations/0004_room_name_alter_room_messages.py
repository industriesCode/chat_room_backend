# Generated by Django 5.0.3 on 2024-03-06 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_room', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='name',
            field=models.TextField(default='test', max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='room',
            name='messages',
            field=models.JSONField(default=dict),
        ),
    ]
# Generated by Django 4.2.4 on 2023-08-10 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrating',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.book'),
        ),
        migrations.AddField(
            model_name='userrating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
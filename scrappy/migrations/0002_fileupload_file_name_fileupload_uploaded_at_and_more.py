# Generated by Django 4.2 on 2023-04-28 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrappy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='file_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='fileupload',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='fileupload',
            name='file',
            field=models.FileField(null=True, upload_to='media/'),
        ),
    ]

# Generated by Django 3.1.1 on 2021-08-27 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapi_UDE_v1', '0003_auto_20210812_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='udeupload',
            name='img',
            field=models.FileField(upload_to='dicom_files/'),
        ),
    ]
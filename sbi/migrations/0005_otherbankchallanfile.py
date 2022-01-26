# Generated by Django 4.0.1 on 2022-01-26 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sbi', '0004_challanfile_cash_deposit'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtherBankChallanFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0)),
                ('challanfile', models.FileField(upload_to='chalan/')),
                ('uploading_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

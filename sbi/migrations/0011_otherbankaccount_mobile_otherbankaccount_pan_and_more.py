# Generated by Django 4.0.1 on 2022-04-16 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sbi', '0010_applicant_rename_telephone_otherbankaccount_bank_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='otherbankaccount',
            name='mobile',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='otherbankaccount',
            name='pan',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='challanfile',
            name='challanfile',
            field=models.FileField(upload_to='chalan/sbibank/'),
        ),
        migrations.AlterField(
            model_name='otherbankchallanfile',
            name='challanfile',
            field=models.FileField(upload_to='chalan/otherbank/'),
        ),
    ]

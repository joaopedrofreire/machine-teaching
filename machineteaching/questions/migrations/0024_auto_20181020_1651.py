# Generated by Django 2.1 on 2018-10-20 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0023_userprofile_strategy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='strategy',
            field=models.CharField(choices=[('random', 'random'), ('eer', 'eer')], max_length=10),
        ),
    ]

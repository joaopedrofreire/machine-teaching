# Generated by Django 2.2.5 on 2020-07-28 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0052_auto_20200728_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='professor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='questions.Professor'),
        ),
    ]

# Generated by Django 2.2.5 on 2020-11-17 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0064_auto_20201117_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='prof_class',
            field=models.ManyToManyField(related_name='professor', to='questions.OnlineClass'),
        ),
    ]
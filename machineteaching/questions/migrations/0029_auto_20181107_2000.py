# Generated by Django 2.1.3 on 2018-11-07 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0028_userlog_error_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlog',
            name='error_type',
            field=models.CharField(choices=[('C', 'Conceptual'), ('S', 'Syntax'), ('D', 'Distraction')], default='D', max_length=2),
        ),
    ]
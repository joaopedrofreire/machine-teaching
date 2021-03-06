# Generated by Django 2.2.1 on 2019-08-08 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0032_merge_20190508_1649'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnlineClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='professor',
            field=models.CharField(blank=True, choices=[('carla', 'Carla'), ('joao', 'João Carlos'), ('hugo', 'Hugo'), ('fernanda', 'Fernanda'), ('kleber', 'Kleber'), ('cadu', 'Cadu'), ('alan', 'Alan'), ('evandro', 'Evandro')], max_length=30),
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prof_class', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='questions.OnlineClass')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='questions.OnlineClass'),
        ),
    ]

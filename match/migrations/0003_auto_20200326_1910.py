# Generated by Django 3.0.4 on 2020-03-26 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0002_auto_20200326_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='skills',
            field=models.ManyToManyField(blank=True, null=True, to='match.Skill'),
        ),
    ]

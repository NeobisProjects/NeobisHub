# Generated by Django 2.2 on 2019-10-15 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20191015_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('c', 'Завершенный'), ('f', 'Заморожен'), ('a', 'Активный')], max_length=5),
        ),
    ]

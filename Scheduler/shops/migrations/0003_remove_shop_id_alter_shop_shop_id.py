# Generated by Django 4.0.4 on 2022-05-19 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0002_rename_shops_shop'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='id',
        ),
        migrations.AlterField(
            model_name='shop',
            name='shop_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
# Generated by Django 4.0.4 on 2022-05-19 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee_Availability',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('initials', models.CharField(max_length=5)),
                ('available_1', models.BinaryField(default=0)),
                ('available_2', models.BinaryField(default=0)),
                ('available_3', models.BinaryField(default=0)),
                ('available_4', models.BinaryField(default=0)),
                ('available_5', models.BinaryField(default=0)),
                ('available_6', models.BinaryField(default=0)),
                ('available_7', models.BinaryField(default=0)),
                ('available_8', models.BinaryField(default=0)),
                ('available_9', models.BinaryField(default=0)),
                ('available_10', models.BinaryField(default=0)),
                ('available_11', models.BinaryField(default=0)),
                ('available_12', models.BinaryField(default=0)),
                ('available_13', models.BinaryField(default=0)),
                ('available_14', models.BinaryField(default=0)),
                ('available_15', models.BinaryField(default=0)),
                ('available_16', models.BinaryField(default=0)),
                ('available_17', models.BinaryField(default=0)),
                ('available_18', models.BinaryField(default=0)),
                ('available_19', models.BinaryField(default=0)),
                ('available_20', models.BinaryField(default=0)),
                ('available_21', models.BinaryField(default=0)),
                ('available_22', models.BinaryField(default=0)),
                ('available_23', models.BinaryField(default=0)),
                ('available_24', models.BinaryField(default=0)),
                ('available_25', models.BinaryField(default=0)),
                ('available_26', models.BinaryField(default=0)),
                ('available_27', models.BinaryField(default=0)),
                ('available_28', models.BinaryField(default=0)),
                ('available_29', models.BinaryField(default=0)),
                ('available_30', models.BinaryField(default=0)),
                ('available_31', models.BinaryField(default=0)),
            ],
        ),
    ]
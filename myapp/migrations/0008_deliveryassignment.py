# Generated by Django 5.1 on 2024-10-16 06:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_alter_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_date', models.DateTimeField(auto_now_add=True)),
                ('delivery_boy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.deliveryboy')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myapp.order')),
            ],
        ),
    ]

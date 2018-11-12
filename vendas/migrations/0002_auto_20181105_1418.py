# Generated by Django 2.1.2 on 2018-11-05 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itempedido',
            name='desconto',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='venda',
            name='desconto',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='venda',
            name='impostos',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
# Generated by Django 2.1.2 on 2018-11-13 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0005_auto_20181113_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itempedido',
            name='produto',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='produtos.Produto'),
            preserve_default=False,
        ),
    ]
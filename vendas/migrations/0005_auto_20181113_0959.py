# Generated by Django 2.1.2 on 2018-11-13 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0004_auto_20181106_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itempedido',
            name='produto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='produtos.Produto'),
        ),
    ]

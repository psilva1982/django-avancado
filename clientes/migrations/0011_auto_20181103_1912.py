# Generated by Django 2.1.2 on 2018-11-03 22:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0010_venda_nfe_emitida'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemPedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qtde', models.FloatField(default=0.0)),
                ('desconto', models.DecimalField(decimal_places=2, max_digits=5)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.Produto')),
            ],
        ),
        migrations.RemoveField(
            model_name='venda',
            name='produtos',
        ),
        migrations.AddField(
            model_name='itempedido',
            name='venda',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.Venda'),
        ),
    ]

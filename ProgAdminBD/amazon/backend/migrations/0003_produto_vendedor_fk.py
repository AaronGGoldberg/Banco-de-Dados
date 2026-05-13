from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_vendedor_produto'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='vendedor',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='produtos',
                to='backend.vendedor',
            ),
        ),
    ]
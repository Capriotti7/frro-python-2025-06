from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0002_remove_pago_concepto_deuda_concepto_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='conceptopago',
            name='tipo',
            field=models.CharField(
                choices=[
                    ('CUOTA_MENSUAL', 'Cuota Mensual'),
                    ('MATRICULA', 'Matrícula'),
                    ('EXAMEN', 'Derecho de Examen'),
                    ('OTRO', 'Otro'),
                ],
                default='OTRO',
                max_length=20,
            ),
        ),
    ]

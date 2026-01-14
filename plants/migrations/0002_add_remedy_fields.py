# Generated manually to add missing fields to Remedy model
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='remedy',
            name='symptom',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='remedy',
            name='usage',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='remedy',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='remedy',
            name='plant',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.CASCADE, to='plants.plant'),
        ),
    ]

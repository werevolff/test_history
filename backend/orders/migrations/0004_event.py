# Generated by Django 3.1.7 on 2021-03-28 06:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0003_orderitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('event_type', models.CharField(choices=[('created', 'created'), ('updated', 'updated'), ('transition', 'transition')], max_length=10, verbose_name='event type')),
                ('subtype', models.CharField(choices=[('created', 'created'), ('updated', 'updated'), ('transition', 'transition')], max_length=255, verbose_name='subtype')),
                ('snapshot', models.JSONField(verbose_name='snapshot')),
                ('difference', models.JSONField(blank=True, null=True, verbose_name='difference')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='orders.order', verbose_name='order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='events', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
                'ordering': ('-created',),
            },
        ),
    ]

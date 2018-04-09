# Generated by Django 2.0.4 on 2018-04-08 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20180408_0929'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameRound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player1_move', models.CharField(max_length=10)),
                ('player2_move', models.CharField(max_length=10)),
                ('round_winner', models.CharField(blank=True, max_length=255)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rounds', to='api.Game')),
            ],
        ),
    ]

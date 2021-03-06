# Generated by Django 3.1.5 on 2021-02-01 21:39

from django.db import migrations, models
import django.db.models.deletion
import tictactoe.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('IN', 'Incomplete'), ('WN', 'Win'), ('DR', 'Draw')], default='IN', max_length=2)),
                ('grid', models.CharField(default=tictactoe.utils.empty_game_grid, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.CharField(choices=[('O', 'Noughts'), ('X', 'Crosses')], default='O', max_length=2)),
                ('coords', models.CharField(max_length=100)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moves', to='tictactoe.game')),
            ],
        ),
    ]

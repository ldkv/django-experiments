# Generated by Django 5.2 on 2025-04-30 18:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("experiments", "0002_experiment20m_experiment5m"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Experiment",
            new_name="Experiment10M",
        ),
        migrations.RenameIndex(
            model_name="experiment10m",
            new_name="experiment10m_name_index",
            old_name="experiments_first_n_2a680d_idx",
        ),
        migrations.RenameIndex(
            model_name="experiment20m",
            new_name="experiment20m_name_index",
            old_name="experiments_first_n_1c78fe_idx",
        ),
        migrations.RenameIndex(
            model_name="experiment5m",
            new_name="experiment5m_name_index",
            old_name="experiments_first_n_bc758b_idx",
        ),
    ]

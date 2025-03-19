# Generated by Django 5.1.6 on 2025-03-19 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0030_alter_leaderboardentry_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="leaderboardentry",
            options={"ordering": ["-points"], "verbose_name_plural": "Leaderboard Entries"},
        ),
        migrations.RenameField(
            model_name="leaderboardentry",
            old_name="score",
            new_name="challenge_count",
        ),
        migrations.AddField(
            model_name="leaderboardentry",
            name="current_streak",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="leaderboardentry",
            name="highest_streak",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="leaderboardentry",
            name="monthly_points",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="leaderboardentry",
            name="points",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="leaderboardentry",
            name="weekly_points",
            field=models.IntegerField(default=0),
        ),
    ]

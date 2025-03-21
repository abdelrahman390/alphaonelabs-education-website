# Generated by Django 5.1.6 on 2025-03-19 04:46

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0029_challengesubmission_points_awarded_friendleaderboard_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="leaderboardentry",
            options={"ordering": ["-score"], "verbose_name_plural": "Leaderboard Entries"},
        ),
        migrations.RenameField(
            model_name="leaderboardentry",
            old_name="challenge_count",
            new_name="score",
        ),
        migrations.RenameField(
            model_name="leaderboardentry",
            old_name="last_updated",
            new_name="updated_at",
        ),
        migrations.RemoveField(
            model_name="leaderboardentry",
            name="current_streak",
        ),
        migrations.RemoveField(
            model_name="leaderboardentry",
            name="highest_streak",
        ),
        migrations.RemoveField(
            model_name="leaderboardentry",
            name="monthly_points",
        ),
        migrations.RemoveField(
            model_name="leaderboardentry",
            name="points",
        ),
        migrations.RemoveField(
            model_name="leaderboardentry",
            name="weekly_points",
        ),
        migrations.AddField(
            model_name="leaderboardentry",
            name="challenge",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="leaderboard_entries",
                to="web.challenge",
            ),
        ),
        migrations.AddField(
            model_name="leaderboardentry",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="leaderboardentry",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="leaderboard_entries",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

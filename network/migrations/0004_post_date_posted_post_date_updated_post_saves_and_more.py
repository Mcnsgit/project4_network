# Generated by Django 5.0.4 on 2024-04-21 19:37

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("network", "0003_alter_post_id_alter_user_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="date_posted",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="post",
            name="date_updated",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="post",
            name="saves",
            field=models.ManyToManyField(
                blank=True, related_name="blogsave", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="title",
            field=models.CharField(default="Untitled", max_length=100),
        ),
        migrations.AlterField(
            model_name="post",
            name="likes",
            field=models.ManyToManyField(
                blank=True, related_name="blogpost", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", models.TextField(max_length=200)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                (
                    "likes",
                    models.ManyToManyField(
                        blank=True,
                        related_name="blogcomment",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="network.post",
                    ),
                ),
                (
                    "reply",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="network.comment",
                    ),
                ),
            ],
        ),
    ]

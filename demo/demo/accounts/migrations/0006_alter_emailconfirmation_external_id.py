# Generated by Django 4.2.10 on 2024-02-26 00:33

from django.db import migrations
import shortuuid.django_fields


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0005_auto_20210511_1956"),
    ]

    operations = [
        migrations.AlterField(
            model_name="emailconfirmation",
            name="external_id",
            field=shortuuid.django_fields.ShortUUIDField(
                alphabet=None, length=22, max_length=22, prefix=""
            ),
        ),
    ]

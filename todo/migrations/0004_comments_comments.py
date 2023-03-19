# Generated by Django 4.1.7 on 2023-03-19 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_remove_comments_photos_comments_images_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='comments',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_on_comments', to='todo.comments'),
        ),
    ]

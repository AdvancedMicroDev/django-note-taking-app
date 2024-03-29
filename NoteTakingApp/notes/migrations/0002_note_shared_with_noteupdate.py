# Generated by Django 5.0.2 on 2024-02-19 23:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='shared_with',
            field=models.ManyToManyField(blank=True, related_name='notes_shared', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='NoteUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updates', to='notes.note')),
            ],
        ),
    ]

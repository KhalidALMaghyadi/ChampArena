# Generated by Django 5.0.6 on 2024-12-16 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='champarena', max_length=100)),
                ('first_name', models.CharField(max_length=64, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=64, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('topic', models.CharField(choices=[('general', 'General'), ('support', 'Support Request'), ('feedback', 'Feedback or Suggestions'), ('complaint', 'Complaint or Issue')], default='general', max_length=64)),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
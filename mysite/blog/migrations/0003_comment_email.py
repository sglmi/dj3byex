# Generated by Django 4.0.3 on 2022-03-08 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='email',
            field=models.EmailField(default='hello@mail.com', max_length=254),
            preserve_default=False,
        ),
    ]
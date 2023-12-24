# Generated by Django 4.2.3 on 2023-10-18 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileApp', '0012_bronzebadge_goldbadge_silverbadge_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Bronze Badge Title', max_length=50)),
                ('description', models.TextField(blank=True, default='Bronze Badge Description')),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='badges/')),
            ],
            options={
                'verbose_name': 'Badge',
                'verbose_name_plural': 'Badge',
            },
        ),
        migrations.DeleteModel(
            name='Badges',
        ),
        migrations.DeleteModel(
            name='bronzeBadge',
        ),
        migrations.DeleteModel(
            name='goldBadge',
        ),
        migrations.DeleteModel(
            name='silverBadge',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='badge',
            field=models.ManyToManyField(related_name='Badges', to='profileApp.badge'),
        ),
    ]
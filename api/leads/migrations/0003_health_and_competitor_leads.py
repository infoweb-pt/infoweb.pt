from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_toolcontactlead'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebsiteHealthScorecardLead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('url', models.CharField(max_length=500)),
                ('score', models.PositiveSmallIntegerField()),
                ('checks', models.JSONField()),
                ('fixes', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Website Health Scorecard Lead',
                'verbose_name_plural': 'Website Health Scorecard Leads',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CompetitorVisibilityGapLead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('score', models.PositiveSmallIntegerField()),
                ('answers', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Competitor Visibility Gap Lead',
                'verbose_name_plural': 'Competitor Visibility Gap Leads',
                'ordering': ['-created_at'],
            },
        ),
    ]

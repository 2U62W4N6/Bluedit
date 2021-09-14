# Generated by Django 3.0.2 on 2020-01-23 21:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=5000)),
                ('created', models.DateField(default=django.utils.timezone.now)),
                ('votes', models.IntegerField(default=0)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', related_query_name='authors', to=settings.AUTH_USER_MODEL)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='subBluedit.Comment')),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
            },
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=1000)),
                ('created', models.DateField(default=django.utils.timezone.now)),
                ('type', models.CharField(choices=[('F', 'Funny'), ('N', 'NSFW'), ('E', 'Educational'), ('S', 'Sport'), ('A', 'Art'), ('', '')], default='', max_length=1)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', related_query_name='owners', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Forum',
                'verbose_name_plural': 'Foren',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('text', models.TextField(blank=True, default='', max_length=5000)),
                ('media', models.URLField(default='')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('votes', models.IntegerField(default=0)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ops', related_query_name='op', to=settings.AUTH_USER_MODEL)),
                ('forum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subBluedit.Forum')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='PostVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subBluedit.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postvoter', related_query_name='postvoters', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'postvote',
                'verbose_name_plural': 'postvotes',
            },
        ),
        migrations.CreateModel(
            name='CommentVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subBluedit.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentvoter', related_query_name='commentvoters', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'commentvote',
                'verbose_name_plural': 'commentvotes',
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subBluedit.Post'),
        ),
        migrations.CreateModel(
            name='Abo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('O', 'Owner'), ('A', 'Admin'), ('S', 'Supervisor'), ('N', 'Normal'), ('B', 'Banned')], default='N', max_length=1)),
                ('forum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subBluedit.Forum')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', related_query_name='subscribers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Abo',
                'verbose_name_plural': 'Abos',
            },
        ),
    ]
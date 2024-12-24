# Generated by Django 5.0.2 on 2024-05-11 05:13

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authtoken', '0003_tokenproxy'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DashboardPermModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Uploaded_File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_file', models.FileField(upload_to='tmp/')),
            ],
        ),
        migrations.CreateModel(
            name='APIcredentials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token_uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('is_production_key', models.BooleanField(default=False)),
                ('is_internal_key', models.BooleanField(default=False)),
                ('is_validated', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credential_owner', to=settings.AUTH_USER_MODEL)),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authtoken.token')),
                ('token_user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='token_username', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DashboardUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_role', models.CharField(choices=[('admin', 'admin'), ('super_admin', 'super_admin'), ('company', 'company'), ('developer', 'developer')], default='developer', max_length=20)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('internal_token', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='apidashboard.apicredentials')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dashboard_user', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SuperAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slave_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slave_user', to='apidashboard.dashboardusers')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='superadmin_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Companies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(default='', max_length=255)),
                ('company_uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('company_email', models.CharField(default='', max_length=255)),
                ('company_telno', models.CharField(default='', max_length=255)),
                ('company_doc', models.FileField(null=True, upload_to='uploads/')),
                ('verification_status', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_owner', to=settings.AUTH_USER_MODEL)),
                ('company_docs', models.ManyToManyField(null=True, related_name='company_docs', to='apidashboard.uploaded_file')),
            ],
        ),
        migrations.CreateModel(
            name='XAPIKeys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_production', models.BooleanField(default=False)),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authtoken.token')),
            ],
        ),
    ]

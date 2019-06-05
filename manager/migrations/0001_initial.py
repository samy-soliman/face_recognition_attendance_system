# Generated by Django 2.2 on 2019-06-05 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('pathToEmpeddings', models.CharField(max_length=200)),
                ('idfk_company', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='accounts.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('idfk_company', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='accounts.Company')),
                ('idfk_grade', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='manager.Grade')),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('idfk_course', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='manager.Course')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='idfk_grade',
            field=models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='manager.Grade'),
        ),
        migrations.AddField(
            model_name='course',
            name='idfk_instructor',
            field=models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='accounts.Instructor'),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField()),
                ('idfk_lecture', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='manager.Lecture')),
                ('idfk_student', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='manager.Student')),
            ],
            options={
                'unique_together': {('idfk_lecture', 'idfk_student')},
            },
        ),
    ]

# Generated by Django 3.1.2 on 2020-10-25 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название подразделения')),
            ],
            options={
                'verbose_name': 'Подразделение',
                'verbose_name_plural': 'Подразделения',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_day', models.CharField(choices=[('Понедельник', 'Понедельник'), ('Вторник', 'Вторник'), ('Среда', 'Среда'), ('Четверг', 'Четверг'), ('Пятница', 'Пятница'), ('Суббота', 'Суббота'), ('Воскресенье', 'Воскресенье')], max_length=20, verbose_name='День недели')),
            ],
            options={
                'verbose_name': 'меню',
            },
        ),
        migrations.CreateModel(
            name='MenuStructure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mealtime_type', models.CharField(choices=[('Завтрак', 'Завтрак'), ('Обед', 'Обед'), ('Ужин', 'Ужин')], max_length=20, verbose_name='Тип приема пищи')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='control.menu')),
            ],
            options={
                'verbose_name': 'Структура меню',
                'verbose_name_plural': 'Структура меню',
            },
        ),
        migrations.CreateModel(
            name='Military',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Имя')),
                ('rank', models.CharField(choices=[('ряд.', 'рядовой'), ('ефр', 'ефрейтор'), ('мл. с-т', 'младший сержант'), ('с-т', 'сержант'), ('ст. с-т', 'старший сержант'), ('пр-к', 'прапорщик'), ('ст пр-к', 'старший прапорщик'), ('мл. л-т', 'младший лейтенант'), ('л-т', 'лейтенант'), ('ст. л-т', 'старший лейтенант'), ('к-н', 'капитан'), ('м-р', 'майор'), ('подп-к', 'подполковник'), ('п-к', 'полковник')], max_length=100, verbose_name='Воинское звание')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='control.company')),
            ],
            options={
                'verbose_name': 'военнослужащий',
                'verbose_name_plural': 'Военнослужащие',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата приема пищи')),
                ('military_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='control.military', verbose_name='Военнослужащий')),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Тип блюда')),
            ],
            options={
                'verbose_name': 'тип блюда',
                'verbose_name_plural': 'Типы блюд',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название блюда')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='control.producttype')),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_structure', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='control.menustructure')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='control.order')),
                ('products', models.ManyToManyField(to='control.Product', verbose_name='Блюда')),
            ],
            options={
                'verbose_name': 'Заказ на прием пищи',
                'verbose_name_plural': 'Заказы на приемы пищи',
            },
        ),
        migrations.AddField(
            model_name='menustructure',
            name='products',
            field=models.ManyToManyField(to='control.Product', verbose_name='Продукты'),
        ),
    ]

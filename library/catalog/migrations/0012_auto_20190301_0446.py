# Generated by Django 2.1.3 on 2019-03-01 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_auto_20190221_0321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='due_back',
            field=models.DateField(blank=True, help_text='yy-mm-dd', null=True),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='due_date',
            field=models.DateField(blank=True, help_text='yy-mm-dd', null=True),
        ),
    ]
# Generated by Django 4.2.7 on 2023-11-01 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('expenseId', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('expense_type', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mobile_number', models.CharField(max_length=15)),
                ('simplify_expenses', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('share_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('share_type', models.CharField(max_length=10)),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='splitwise.expense')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='splitwise.user')),
            ],
        ),
        migrations.AddField(
            model_name='expense',
            name='payer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='splitwise.user'),
        ),
    ]

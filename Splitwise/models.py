from django.db import models

# Create your models here.


class User(models.Model):
    userId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    simplify_expenses = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Expense(models.Model):
    expenseId = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payer = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, through="ExpenseParticipant")
    expense_type = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class ExpenseParticipant(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share_amount = models.DecimalField(max_digits=10, decimal_places=2)
    share_type = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user} in {self.expense}"

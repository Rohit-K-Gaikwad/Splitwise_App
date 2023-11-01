from celery import shared_task
from django.core.mail import send_mail
from utils.utils import calculate_simplified_balances
from .models import User


@shared_task
def send_weekly_reminder_email(user_id):
    user = User.objects.get(pk=user_id)

    # Calculate the balance
    balances = calculate_simplified_balances(user)

    subject = "Weekly Expense Reminder"
    message = "Here is your weekly expense summary..."
    from_email = "rohitgaikwad.connect@gmail.com"

    # Construct the email content
    subject = "Weekly Expense Reminder"
    message = "Here is your weekly expense summary:\n\n"

    for debtor, amount in balances.items():
        if amount < 0:
            message += f"You owe {debtor.name}: {abs(amount)} INR\n"

    # Include any other relevant content in the email message.

    from_email = "your@email.com"
    recipient_list = [user.email]

    # Send the email
    send_mail(subject, message, from_email, recipient_list)

from Splitwise.models import Expense


def calculate_balances(expense):
    """To calculate the balance from expenses made"""
    balances = {}
    for participant in expense.participants.all():
        if participant.user == expense.payer:
            continue  # The payer doesn't owe themselves

        share_amount = participant.share_amount
        if participant.share_type == "EXACT":
            share_amount = participant.share_amount
        elif participant.share_type == "PERCENT":
            share_amount = (expense.amount * participant.share_amount) / 100

        if participant.user in balances:
            balances[participant.user] += share_amount
        else:
            balances[participant.user] = share_amount

        if expense.payer in balances:
            balances[expense.payer] -= share_amount
        else:
            balances[expense.payer] = -share_amount

    return balances


def calculate_simplified_balances(user):
    """Calculating simplified balance for each user"""
    balances = {}  # Initialize the balances
    user_expenses = Expense.objects.filter(payer=user)
    for expense in user_expenses:
        participants = expense.participants.all()
        for participant in participants:
            if participant != user:
                # Calculate the net amount owed by or to the user
                share_amount = participant.share_amount
                if participant.share_type == "EXACT":
                    share_amount = participant.share_amount
                elif participant.share_type == "PERCENT":
                    share_amount = (expense.amount * participant.share_amount) / 100
                if participant in balances:
                    balances[participant] += share_amount
                else:
                    balances[participant] = share_amount
    return balances

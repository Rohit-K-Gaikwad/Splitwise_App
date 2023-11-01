from django.shortcuts import render
from rest_framework import views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import (
    UserSerializer,
    ExpenseSerializer,
    ExpenseParticipantsSerializer,
)
from decimal import Decimal

from .models import User, Expense, ExpenseParticipant
from utils.utils import calculate_balances, calculate_simplified_balances
from .tasks import send_weekly_reminder_email


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def create_exact_expense(payer, description, amounts, participants):
    # Create the expense
    expense = Expense.objects.create(
        payer=payer, description=description, amount=sum(amounts)
    )
    # Split the expense with exact amounts
    for i, participant in enumerate(participants):
        ExpenseParticipant.objects.create(
            expense=expense,
            user=participant,
            share_amount=amounts[i],
            share_type="EXACT",
        )

    return expense


def create_percentage_expense(
    request, payer, description, amounts, participants, percentages
):
    # Create the expense
    expense = Expense.objects.create(
        payer=payer, description=description, amount=sum(amounts)
    )

    # Split the expense based on percentages
    total_percentage = sum(percentages)
    for i, participant in enumerate(participants):
        share_amount = (amounts[i] * percentages[i]) / total_percentage
        ExpenseParticipant.objects.create(
            expense=expense,
            user=participant,
            share_amount=share_amount,
            share_type="PERCENT",
        )

    return expense


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    @action(detail=True, methods=["get"])
    def participants(self, request, pk=None):
        expense = self.get_object()
        participants = ExpenseParticipant.object.filter(expense=expense)
        serializer = ExpenseParticipantsSerializer(participants, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            # create the expense
            expense = serializer.save()

            # Split the expense equally among the participants
            participants = expense.participants.all()
            num_participants = len(participants)
            share_amount = expense.amount / num_participants

            for participant in participants:
                ExpenseParticipant.objects.create(
                    expense=expense,
                    user=participant.user,
                    share_amount=share_amount,
                    share_type="EQUAL",
                )

            # Calculate and update balances
            balances = calculate_balances(expense)
            for user, balance in balances.items():
                user.balance += balance
                user.save()

            return Response(ExpenseSerializer(expense).data)
        else:
            return Response(serializer.errors, status=400)

    def create_exact_expense(request):
        payer = User.objects.get(pk=1)  # Assuming the payer is User with ID 1
        description = "Shopping"
        amounts = [Decimal("370"), Decimal("880")]
        participants = [payer, User.objects.get(pk=2), User.objects.get(pk=3)]

        expense = create_exact_expense(
            request, payer, description, amounts, participants
        )

        return Response(ExpenseSerializer(expense).data)

    def create_percentage_expense(request):
        payer = User.objects.get(pk=1)  # Assuming the payer is User with ID 1
        description = "Dinner"
        amounts = [
            1200,
            0,
            0,
            0,
        ]  # Total amount is 1200, distributed among 4 participants
        participants = [
            payer,
            User.objects.get(pk=2),
            User.objects.get(pk=3),
            User.objects.get(pk=4),
        ]
        percentages = [40, 20, 20, 20]

        expense = create_percentage_expense(
            request, payer, description, amounts, participants, percentages
        )

        return Response(ExpenseSerializer(expense).data)


class ParticipantsViewSet(viewsets.ModelViewSet):
    queryset = Expense.participants.objects.get()    # Intermediate model for Expense Participants
    serializer_class = Expense.participants.Serializer


class SimplifyExpenseView(views.APIView):
    def put(self, request, userID):
        user = User.objects.get(pk=userID)

        user.simplify_expenses = not user.simplify_expenses
        user.save()

        return Response({"message": "Expense simplification toggled."})


class UserBalancesView(views.APIView):
    def get(self, request, userID):
        user = User.objects.get(pk=userID)
        if user.simplify_expenses:
            balances = calculate_simplified_balances(user)
        else:
            balances = calculate_balances(user)
        return Response(balances)


class WeeklyReminderView(views.APIView):
    def get(self, request, userId):
        user = User.objects.get(pk=userId)
        # Implement logic to send a weekly reminder email to this user
        # You can use your email sending code here, or use an asynchronous task.
        send_weekly_reminder_email.delay(user.pk)
        return Response({"message": "Weekly reminder email scheduled for sending."})

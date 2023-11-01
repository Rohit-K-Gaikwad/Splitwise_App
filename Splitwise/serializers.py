from rest_framework import serializers
from .models import User, Expense, ExpenseParticipant


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ExpenseParticipantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseParticipant
        fields = "__all__"


class ExpenseSerializer(serializers.ModelSerializer):
    participants = ExpenseParticipantsSerializer(many=True, read_only=True)

    class Meta:
        model = Expense
        fields = "__all__"

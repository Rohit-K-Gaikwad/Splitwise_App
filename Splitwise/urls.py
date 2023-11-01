from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Splitwise.views import (
    UserViewSet,
    ExpenseViewSet,
    UserBalancesView,
    SimplifyExpenseView,
    WeeklyReminderView
  )

router = DefaultRouter()

router.register(r"users", UserViewSet)
router.register(r"expenses", ExpenseViewSet)


urlpatterns = [
    path("splitwise/", include(router.urls)),
    path(
        "splitwise/users/<int:userId>/balances/",
        UserBalancesView.as_view(),
        name="user-balances",
    ),
    path(
        "splitwise/users/<int:userId>/simplify-expenses/",
        SimplifyExpenseView.as_view(),
        name="simplify-expenses",
    ),
    path(
        "splitwise/users/<int:userId>/weekly-reminder/",
        WeeklyReminderView.as_view(),
        name="weekly-reminder",
    ),
]

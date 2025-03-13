from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from chats.views import ConversationViewSet, MessageViewSet, RegisterView, LoginView
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r"conversations", ConversationViewSet)
router.register(r"messages", MessageViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "message/<int:message_id>/history/",
        views.message_history,
        name="message_history",
    ),
    path("delete-account/", views.delete_user, name="delete_user"),
]

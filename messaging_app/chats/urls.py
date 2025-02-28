from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from chats.views import ConversationViewSet, MessageViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

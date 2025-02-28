from rest_framework import serializers
from .models import CustomUser, Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Include sender details

    class Meta:
        model = Message
        fields = ['id', 'sender', 'conversation', 'text', 'timestamp']
        read_only_fields = ['sender', 'conversation', 'timestamp']

# Conversation Serializer (Includes messages)
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)  # Nested users
    messages = MessageSerializer(many=True, read_only=True, source="messages.all")  # Nested messages

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'created_at']

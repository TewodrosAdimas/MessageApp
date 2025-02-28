from rest_framework import serializers
from .models import CustomUser, Conversation, Message

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio', 'profile_picture']

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

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, CustomUser
from .serializers import ConversationSerializer, MessageSerializer

# Conversation ViewSet
class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, and retrieving conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with specified participants.
        """
        participant_ids = request.data.get('participants', [])
        if not participant_ids:
            return Response({"error": "At least one participant is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure all participants exist
        participants = CustomUser.objects.filter(id__in=participant_ids)
        if not participants.exists():
            return Response({"error": "Invalid participant IDs."}, status=status.HTTP_400_BAD_REQUEST)

        # Create conversation and add participants
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.participants.add(request.user)  # Include the creator
        serializer = self.get_serializer(conversation)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Message ViewSet
class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Send a message to an existing conversation.
        """
        conversation_id = request.data.get('conversation')
        text = request.data.get('text')

        # Validate conversation
        conversation = get_object_or_404(Conversation, id=conversation_id)
        if request.user not in conversation.participants.all():
            return Response({"error": "You are not a participant in this conversation."}, status=status.HTTP_403_FORBIDDEN)

        # Create message
        message = Message.objects.create(conversation=conversation, sender=request.user, text=text)
        serializer = self.get_serializer(message)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

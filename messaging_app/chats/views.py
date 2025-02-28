from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from .models import Conversation, Message, CustomUser
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsConversationParticipant, IsMessageSenderOrConversationParticipant
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from .filters import MessageFilter  # Import the filter class

class MessagePagination(PageNumberPagination):
    page_size = 20  # Number of messages per page
    page_size_query_param = 'page_size'  # Allow users to set the page size via query parameter
    max_page_size = 100  # Maximum page size allowed

# Conversation ViewSet
class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, and retrieving conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsConversationParticipant]

    def get_queryset(self):
        """
        Limit the conversations to those that the current user is a participant.
        """
        return Conversation.objects.filter(participants=self.request.user)

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

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """
        Retrieve all messages from a specific conversation.
        """
        conversation = get_object_or_404(Conversation, pk=pk)

        # Ensure the user is part of the conversation before fetching messages
        self.check_object_permissions(request, conversation)

        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

# Message ViewSet
class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageSenderOrConversationParticipant]
    pagination_class = MessagePagination  # Set pagination for this viewset
    filter_backends = (filters.DjangoFilterBackend,)  # Add the filter backend
    filterset_class = MessageFilter  # Apply the MessageFilter for filtering

    def get_queryset(self):
        """
        Limit the messages to the current user's conversations.
        """
        return Message.objects.filter(conversation__participants=self.request.user)

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

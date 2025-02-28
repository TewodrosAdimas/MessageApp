from rest_framework import permissions

class IsConversationParticipant(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation to view or send messages.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant in the conversation
        return request.user in obj.participants.all()


class IsMessageSenderOrConversationParticipant(permissions.BasePermission):
    """
    Custom permission to allow only:
    - The sender of the message
    - Any participant of the conversation
    """

    def has_object_permission(self, request, view, obj):
        # User can access if they are the sender of the message or a participant in the conversation
        return request.user == obj.sender or request.user in obj.conversation.participants.all()

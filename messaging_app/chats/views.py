from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend

class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoints for conversations.
    - list: returns only conversations where request.user is a participant
    - create: supply participant_ids (list of UUIDs) to create; request.user auto-included
    - add_message (action): add message as the authenticated user
    """
    queryset = Conversation.objects.all().prefetch_related('participants', 'messages')
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]
    pagination_class = None  # optional; conversations are often few

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants=user).distinct()

    def create(self, request, *args, **kwargs):
        """
        Expect payload:
        {
          "participant_ids": ["uuid1", "uuid2", ...]
        }
        The creating user is auto-added.
        """
        participant_ids = request.data.get('participant_ids', [])
        if participant_ids and not isinstance(participant_ids, (list, tuple)):
            raise ValidationError({"participant_ids": "Must be a list of UUIDs"})

        conv = Conversation.objects.create()
        conv.participants.add(request.user)

        # Add valid participants
        for uid in participant_ids:
            try:
                u = User.objects.get(user_id=uid)
            except User.DoesNotExist:
                conv.delete()
                raise ValidationError({"participant_ids": f"User {uid} does not exist"})
            conv.participants.add(u)

        conv.save()
        serializer = self.get_serializer(conv)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsParticipantOfConversation])
    def add_message(self, request, pk=None):
        conv = self.get_object()
        if not conv.participants.filter(user_id=request.user.user_id).exists():
            raise PermissionDenied("You are not a participant of this conversation.")

        message_body = request.data.get('message_body')
        if not message_body:
            raise ValidationError({"message_body": "This field is required."})

        msg = Message.objects.create(conversation=conv, sender=request.user, message_body=message_body)
        serializer = MessageSerializer(msg)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    """
    Message endpoints with filtering and pagination.
    - list: messages only from conversations the user participates in
    - create: requires conversation_id in payload; sender forced to request.user
    """
    queryset = Message.objects.all().select_related('sender', 'conversation')
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = MessageFilter
    pagination_class = StandardResultsSetPagination
    ordering_fields = ['sent_at']
    search_fields = ['message_body']

    def get_queryset(self):
        user = self.request.user
        # messages whose conversation includes the user
        return Message.objects.filter(conversation__participants=user).select_related('sender', 'conversation')

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation_id')
        message_body = request.data.get('message_body')

        if not conversation_id:
            raise ValidationError({"conversation_id": "This field is required."})
        if not message_body:
            raise ValidationError({"message_body": "This field is required."})

        try:
            conv = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            raise ValidationError({"conversation_id": "Conversation not found."})

        if not conv.participants.filter(user_id=request.user.user_id).exists():
            raise PermissionDenied("You are not a participant of the conversation.")

        msg = Message.objects.create(conversation=conv, sender=request.user, message_body=message_body)
        serializer = self.get_serializer(msg)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

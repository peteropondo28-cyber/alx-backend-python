import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class UnreadMessagesManager(models.Manager):
    """
    Custom manager to return unread messages for a user.
    Use .for_user(user) to get unread messages.
    """

    def for_user(self, user):
        # .only to fetch only required fields
        return self.get_queryset().filter(receiver=user, read=False).only(
            'id', 'sender_id', 'receiver_id', 'content', 'timestamp'
        )


class Conversation(models.Model):
    """
    Optional conversation grouping model. Not strictly required but useful
    if you want conversation-level grouping of messages.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    """
    Message model with sender, receiver, content, timestamp, edited flag,
    parent_message for threaded replies, and read flag.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, null=True, blank=True, on_delete=models.CASCADE, related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='messages_sent', on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='messages_received', on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies'
    )

    objects = models.Manager()
    unread = UnreadMessagesManager()

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message {self.id} from {self.sender}"

    def get_thread(self):
        """
        Return a nested dict representing this message and all replies (recursive).
        Efficiently uses prefetching if the instance was fetched with prefetch_related('replies').
        """
        def _gather(msg):
            data = {
                'id': msg.id,
                'sender_id': msg.sender_id,
                'receiver_id': msg.receiver_id,
                'content': msg.content,
                'timestamp': msg.timestamp,
                'edited': msg.edited,
                'read': msg.read,
                'replies': []
            }
            # if replies prefetched, iterating won't hit DB
            for r in getattr(msg, 'replies_cache', msg.replies.all()):
                data['replies'].append(_gather(r))
            return data

        # Optionally populate replies_cache to avoid extra queries
        # when called on a queryset: qs = Message.objects.filter(...).prefetch_related('replies')
        return _gather(self)


class MessageHistory(models.Model):
    """
    Tracks previous versions of a message's content.
    Created by pre_save signal before message is edited.
    """
    id = models.AutoField(primary_key=True)
    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-edited_at']

    def __str__(self):
        return f"History for {self.message.id} at {self.edited_at}"


class Notification(models.Model):
    """
    Notification created for receiving user when a new message is posted.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='notification_for', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="New Message")
    body = models.TextField(blank=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification {self.id} -> {self.user}"

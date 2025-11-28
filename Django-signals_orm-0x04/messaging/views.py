from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views import View

from .models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def delete_user(request):
    """
    Allow a user to delete their own account and cascade delete related data.
    """
    user = request.user
    # Optionally confirm via POST payload; here we delete directly
    user.delete()
    return JsonResponse({'status': 'deleted'}, status=200)


# cache this view for 60 seconds
@cache_page(60)
@login_required
def conversation_messages(request, conversation_id):
    """
    Return messages for a conversation, optimized with select_related and prefetch_related.
    Only participants can access.
    """
    conversation = get_object_or_404(Conversation, pk=conversation_id)
    if not conversation.participants.filter(pk=request.user.pk).exists():
        return HttpResponseForbidden("Not a participant")

    # Use select_related to get sender/receiver in same query; prefetch replies
    qs = Message.objects.filter(conversation=conversation, parent_message__isnull=True).select_related(
        'sender', 'receiver'
    ).prefetch_related('replies__sender', 'replies__replies')

    # Build a serializable structure with nested replies
    data = []
    for m in qs:
        # to avoid hitting DB for replies iterating, assign cache attribute
        m.replies_cache = list(m.replies.select_related('sender').all())
        data.append(m.get_thread())

    return JsonResponse({'messages': data}, status=200, safe=False)


@login_required
def mark_as_read(request, message_id):
    """
    Mark a message as read (if receiver is request.user)
    """
    msg = get_object_or_404(Message, pk=message_id)
    if msg.receiver != request.user:
        return HttpResponseForbidden("Not allowed")
    msg.read = True
    msg.save()
    return JsonResponse({'status': 'ok'})

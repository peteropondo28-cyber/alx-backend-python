from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from .models import Message


# -----------------------------------------------------
# 1. Delete user (post_delete signal handles cleanup)
# -----------------------------------------------------
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return JsonResponse({"status": "User deleted successfully"})


# -----------------------------------------------------
# 2. Use the custom unread manager
# -----------------------------------------------------
def unread_inbox(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Use custom manager + optimized `.only()`
    unread_messages = Message.unread.for_user(user)

    data = [
        {
            "id": m.id,
            "sender": m.sender.username,
            "content": m.content,
            "timestamp": m.timestamp,
        }
        for m in unread_messages
    ]

    return JsonResponse(data, safe=False)


# -----------------------------------------------------
# 3. Recursive threaded message fetcher
# -----------------------------------------------------
def get_replies(message):
    # Replies are prefetched in the parent queryset, no extra DB hits  
    return [
        {
            "id": reply.id,
            "sender": reply.sender.username,
            "content": reply.content,
            "timestamp": reply.timestamp,
            "replies": get_replies(reply),
        }
        for reply in message.replies.all()
    ]


# -----------------------------------------------------
# 4. Cached conversation messages (60 seconds)
# Uses both custom manager & optimized ORM
# -----------------------------------------------------
@cache_page(60)
def conversation_messages(request, user1, user2):
    messages = (
        Message.objects
        .filter(sender_id__in=[user1, user2], receiver_id__in=[user1, user2])
        .select_related("sender", "receiver")         # reduces sender/receiver queries
        .prefetch_related("replies", "replies__sender")  # optimizes threaded replies
        .order_by("timestamp")
    )

    response_data = []

    for msg in messages:
        response_data.append({
            "id": msg.id,
            "sender": msg.sender.username,
            "receiver": msg.receiver.username,
            "content": msg.content,
            "timestamp": msg.timestamp,
            "replies": get_replies(msg),
        })

    return JsonResponse(response_data, safe=False)

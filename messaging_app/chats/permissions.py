from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Permission:
      - User must be authenticated (enforced globally by default settings).
      - For object-level access: user must be in conversation.participants.
      - For actions like create/list: authenticated users allowed (views filter results).
    """

    def has_permission(self, request, view):
        # Require authentication at top-level (settings also enforces this).
        if not request.user or not request.user.is_authenticated:
            return False

        # Allow list and create actions; viewset will filter results to user's scope.
        if view.action in ('list', 'create'):
            return True

        # For other actions like retrieve/update/destroy, fallback to object permission
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        # If the object is a Conversation
        if hasattr(obj, 'participants'):
            return obj.participants.filter(user_id=user.user_id).exists()

        # If the object is a Message, check its conversation's participants
        if hasattr(obj, 'conversation'):
            return obj.conversation.participants.filter(user_id=user.user_id).exists()

        return False

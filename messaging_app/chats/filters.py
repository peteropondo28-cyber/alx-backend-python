import django_filters
from .models import Message
from django_filters import rest_framework as filters

class MessageFilter(filters.FilterSet):
    """
    Filters available:
      - conversation: filter by conversation UUID
      - sender: filter by sender UUID
      - sent_after: ISO datetime >=
      - sent_before: ISO datetime <=
      - search: substring search on message_body
    """
    conversation = filters.UUIDFilter(field_name='conversation__conversation_id')
    sender = filters.UUIDFilter(field_name='sender__user_id')
    sent_after = filters.IsoDateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_before = filters.IsoDateTimeFilter(field_name='sent_at', lookup_expr='lte')
    search = filters.CharFilter(method='filter_search')

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'sent_after', 'sent_before', 'search']

    def filter_search(self, queryset, name, value):
        return queryset.filter(message_body__icontains=value)

import django_filters
from .models import Message, CustomUser

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.ModelChoiceFilter(queryset=CustomUser.objects.all(), required=False)
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', required=False)
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte', required=False)

    class Meta:
        model = Message
        fields = ['sender', 'start_date', 'end_date']

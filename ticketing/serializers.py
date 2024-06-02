from rest_framework import serializers
from .models import TicketType, Ticket
from event_management.serializers import EventSerializer
from rest_framework.validators import UniqueTogetherValidator

# class TicketTypeSerializer(serializers.ModelSerializer):
#     # event = EventSerializer()
#     # name = serializers.CharField(required=True)
#     # price = serializers.IntegerField(min_value=50)
#     class Meta:
#         model = TicketType
#         fields = ['id', 'name', 'price', 'event']

#         # validators = [
#         #     UniqueTogetherValidator(
#         #         queryset=TicketType.objects.all(),
#         #         fields=['name', 'price', 'event']
#         #     )
#         # ]

#     # def validate_price(self, value):
#     #     if value < 50:
#     #         raise serializers.ValidationError("Price must be greater than 50.")
#     #     return value

class TicketTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    price = serializers.IntegerField()
    event = EventSerializer(read_only=True)

    def create(self, validated_data):
        return TicketType.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance


# class TicketSerializer(serializers.ModelSerializer):
#     event = serializers.SerializerMethodField()
#     ticket_type = serializers.SerializerMethodField()

#     # ticket_type = TicketTypeSerializer()
#     # event = EventSerializer(source = 'ticket_type.event')

#     class Meta:
#         model = Ticket
#         fields = ['id', 'event',  'ticket_type', 'checked_in', 'qr_code']

#     def get_event(self, ticket):
#         event = ticket.ticket_type.event
#         return {
#             'name': event.name,
#             'date': event.date,
#         }

#     def get_ticket_type(self, ticket):
#         ticket_type = ticket.ticket_type
#         return {
#             'name': ticket_type.name,
#             'price': ticket_type.price,
#         }

class TicketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    event = EventSerializer(source = 'ticket_type.event')
    ticket_type = TicketTypeSerializer()
    checked_in = serializers.BooleanField()
    qr_code = serializers.ImageField()

    # def create(self, validated_date):
    #     return Ticket.objects.create(**validated_date)


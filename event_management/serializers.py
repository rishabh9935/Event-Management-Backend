from rest_framework import serializers # type: ignore
from .models import CustomUser, Event, Donor, DonorManagement, Auction


# class DonorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Donor
#         fields = ['id', 'donor_name', 'email']

class DonorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    donor_name = serializers.CharField(max_length=220)
    email = serializers.EmailField()

# class UserSerializer(serializers.ModelSerializer):
#     # password = serializers.CharField(write_only=True)

#     class Meta:
#         model = CustomUser
#         fields = ['id', 'username', 'email', 'password']
        
#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(**validated_data)
#         return user

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=220)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# class EventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = '__all__'


class EventSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=220)
    date = serializers.DateField()
    location = serializers.CharField(max_length=220)
    description = serializers.CharField()
    details = serializers.CharField(default='blank')
    is_private = serializers.BooleanField(default=False)
    photo = serializers.ImageField(required=False)
    bidItem = serializers.CharField(max_length=255, allow_null=True, default=None)
    is_raffle = serializers.BooleanField(default=False)
    image_urls = serializers.CharField(allow_null=True, required=False)

    def create(self, validated_data):
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.date = validated_data.get('date', instance.date)
        instance.location = validated_data.get('location', instance.location)
        instance.description = validated_data.get('description', instance.description)
        instance.details = validated_data.get('details', instance.details)
        instance.is_private = validated_data.get('is_private', instance.is_private)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.bidItem = validated_data.get('bidItem', instance.bidItem)
        instance.is_raffle = validated_data.get('is_raffle', instance.is_raffle)
        instance.image_urls = validated_data.get('image_urls', instance.image_urls)

        instance.save()
        return instance

# class SilentAuctionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Auction
#         fields = ['id', 'user_id', 'event_id', 'bid']
 
#     def validate_bid(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("Bid amount must be greater than zero.")
#         return value

class SilentAuctionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = UserSerializer(read_only=True)
    event_id = EventSerializer(read_only=True)
    bid = serializers.DecimalField(max_digits=10, decimal_places=2)

    def create(self, validated_data):
        return Auction.objects.create(**validated_data) 
    
    def validate_bid(self, value):
        if value <= 0:
            raise serializers.ValidationError("Bid amount must be greater than zero.")
        return value
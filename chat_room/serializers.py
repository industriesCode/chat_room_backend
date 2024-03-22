from rest_framework import serializers
from django.contrib.auth.models import User
from chat_room.models import Room, Messages


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['name', 'created_by', 'created_at', 'updated_at']


class MessagesSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request_method = self.context.get('request').method if 'request' in self.context else None
        print("--------------------------")
        print(request_method)
        print("--------------------------")
        if request_method != 'POST':
            self.fields['sent_by'] = serializers.CharField(source='sent_by.username', read_only=True)

    class Meta:
        model = Messages
        fields = '__all__'

from django.contrib.auth.models import User
from django.http import Http404

from .models import Room, Messages
from rest_framework import status
from django.utils import timezone
from .serializers import UserSerializer, MessagesSerializer
from .serializers import RoomSerializer
from rest_framework.views import APIView
from datetime import timedelta
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.


class UserSignup(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInAPIView(APIView):
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        # Check if username and password are provided
        if username and password:
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)

                # Serialize user data
                user_serializer = UserSerializer(user)
                user_data = user_serializer.data

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': user_data,
                    'message': 'Login successful'
                }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)


class CreateRoom(APIView):
    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        # Get today's date and yesterday's date
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        day_after_yesterday = today - timedelta(days=2)

        # Filter queryset to get rooms created today and yesterday
        rooms_today = Room.objects.filter(created_at__date=today)
        rooms_yesterday = Room.objects.filter(created_at__date=yesterday)
        older_rooms = Room.objects.filter(created_at__date__lt=day_after_yesterday)

        # Serialize queryset for both today and yesterday
        serializer_today = RoomSerializer(rooms_today, many=True)
        serializer_yesterday = RoomSerializer(rooms_yesterday, many=True)
        serializer_older = RoomSerializer(older_rooms, many=True)

        return Response(
            {
                'today': serializer_today.data,
                'yesterday': serializer_yesterday.data,
                'older': serializer_older.data
            },
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk):
        room = Room.objects.get(pk=pk)
        serializer = RoomSerializer(instance=room, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        room = Room.objects.get(pk=pk)
        serializer = RoomSerializer(instance=room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        room = Room.objects.get(pk=pk)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomMessages(APIView):

    def get(self, request):
        try:
            room_name = request.query_params.get('data', '')
            room = Room.objects.get(name=room_name)
            messages = Messages.objects.filter(room=room)
            serializer = MessagesSerializer(messages, many=True)
            return Response(serializer.data)
        except Room.DoesNotExist:
            raise Http404

    def post(self, request):
        request_data = {
            'message': request.data['message'],
            'room': Room.objects.get(name=request.data['room']).pk,
            'sent_by': User.objects.get(username=request.data['sent_by']).pk,
        }

        serializer = MessagesSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

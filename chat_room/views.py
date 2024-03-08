from .models import Room
from rest_framework import status
from .serializers import UserSerializer
from .serializers import RoomSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login

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
                # Log in the user
                login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
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
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

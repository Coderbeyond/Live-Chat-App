from chatapp.serializers import MessageSerializer, UserSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import Message, User
from django.shortcuts import render


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def online_users(self, request, pk=None):
        online_users = User.objects.filter(is_online=True).values('user')
        online_user_ids = [user['user'] for user in online_users]
        queryset = self.queryset.filter(id__in=online_user_ids)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'message': 'Please provide both username and password.'}, status=400)
        user = User.objects.get(username=username,password=password)

        if not user:
            return Response({'message': 'Invalid username or password.'}, status=400)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=200)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(detail=False, methods=['post'])
    def start(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            recipient_id = serializer.validated_data.get('recipient_id')
            recipient = User.objects.get(id=recipient_id)
            
            if recipient.is_online and recipient.is_available:
                message = serializer.save()
                return Response({'message': 'Message sent successfully.', 'message_id': message.id})
            else:
                return Response({'message': 'Recipient is offline or unavailable.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def index(request):
    return render(request, 'index.html')

def roomName(request, room_name):
        return render(request, 'chatroom.html', {'room_name': room_name})
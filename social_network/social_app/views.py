from django.contrib.auth import authenticate, login
from rest_framework import status, viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .serializers import UserSerializer, SignupSerializer, FriendRequestSerializer
from .filters import UserFilter
from django.contrib.auth.models import User
from .models import FriendRequest
from django.utils import timezone
from datetime import timedelta


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

class UserSearchView(APIView):
    def get(self, request):
        search_keyword = request.GET.get('search', '')
        if not search_keyword:
            return Response({"error": "Search keyword is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Apply the filter
        user_filter = UserFilter({'search': search_keyword}, queryset=User.objects.all())
        users = user_filter.qs

        # Paginate the results
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

class SendFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        receiver_id = request.data.get('receiver')
        if not receiver_id:
            return Response({"error": "Receiver ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response({"error": "Receiver not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check the number of friend requests sent in the last minute
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests_count = FriendRequest.objects.filter(
            sender=request.user, 
            created_at__gte=one_minute_ago
        ).count()

        if recent_requests_count >= 3:
            return Response({"error": "You cannot send more than 3 friend requests within a minute"}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        if FriendRequest.objects.filter(sender=request.user, receiver=receiver, status='sent').exists():
            return Response({"error": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendRequest(sender=request.user, receiver=receiver)
        friend_request.save()
        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RespondToFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request_id = request.data.get('request_id')
        action = request.data.get('action')  # 'accept' or 'reject'
        if not request_id or action not in ['accept', 'reject']:
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            friend_request = FriendRequest.objects.get(id=request_id, receiver=request.user)
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

        if action == 'accept':
            friend_request.status = 'accepted'
        elif action == 'reject':
            friend_request.status = 'rejected'
        
        friend_request.save()
        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ListFriendsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Find all accepted friend requests where the current user is either the sender or the receiver
        friends_as_sender = FriendRequest.objects.filter(sender=request.user, status='accepted')
        friends_as_receiver = FriendRequest.objects.filter(receiver=request.user, status='accepted')
        
        friend_ids = set(friends_as_sender.values_list('receiver_id', flat=True)) | set(friends_as_receiver.values_list('sender_id', flat=True))
        friends = User.objects.filter(id__in=friend_ids)

        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data)

class ListPendingFriendRequests(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(receiver=user, status='pending')
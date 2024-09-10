from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('search/', UserSearchView.as_view()),  # Search API route
    path('friend-request/send/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/respond/', RespondToFriendRequestView.as_view(), name='respond-to-friend-request'),
    path('friends/', ListFriendsView.as_view(), name='list-friends'),
    path('friend-request/pending/', ListPendingFriendRequests.as_view(), name='list_pending_friend_requests'),
]

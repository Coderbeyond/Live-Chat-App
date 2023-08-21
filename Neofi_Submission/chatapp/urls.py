from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, MessageViewSet , index, roomName

router = routers.DefaultRouter()
router.register(r'', UserViewSet)
router.register(r'chat', MessageViewSet)

urlpatterns = [
    path('', index, name="index"),
    path('<str:room_name>/', roomName, name='room'),
    path('api/', include(router.urls)),
]

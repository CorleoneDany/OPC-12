from .models import Event, Client, Contract
from django.contrib.auth.models import User
from .serializers import EventSerializer, ClientSerializer, ContractSerializer, UserSerializer
from .permissions import HasClientPermission, HasContractPermission, HasEventPermission, HasUserPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (HasUserPermission, IsAuthenticated)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (HasEventPermission, IsAuthenticated)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (HasClientPermission, IsAuthenticated)


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = (HasContractPermission, IsAuthenticated)

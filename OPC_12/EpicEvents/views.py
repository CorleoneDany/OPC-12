from .models import Event, Client, Contract
from django.contrib.auth.models import User
from .serializers import EventSerializer, ClientSerializer, ContractSerializer, UserSerializer
from .permissions import HasClientPermission, HasContractPermission, HasEventPermission
from django.conf import settings
from rest_framework.response import Response
from rest_framework import viewsets

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

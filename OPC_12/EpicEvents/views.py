from urllib import response
from .models import Event, Client, Contract, ContractStatus
from django.contrib.auth.models import User
from .serializers import EventSerializer, ClientSerializer, ContractSerializer, UserSerializer
from .permissions import HasClientPermission, HasContractPermission, HasEventPermission, HasUserPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (HasUserPermission, IsAuthenticated)

    def destroy(self, request, *args, **kwargs):
        return Response(status=401)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (HasEventPermission, IsAuthenticated)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['Client__LastName', 'Client__Email', 'EventDate']

    def create(self, request, *args, **kwargs):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            contract_status = ContractStatus.objects.create(
                Status=request.data['Status'])
            serializer.save(SupportContact=request.user,
                            EventStatus=contract_status)
            return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        return Response(status=401)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (HasClientPermission, IsAuthenticated)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['LastName', 'Email']

    def create(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(SalesContact=request.user)
            return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        return Response(status=401)


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = (HasContractPermission, IsAuthenticated)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['Client__LastName',
                        'Client__Email', 'DateCreated', 'Amount']

    def create(self, request, *args, **kwargs):
        serializer = ContractSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(SalesContact=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        return Response(status=401)

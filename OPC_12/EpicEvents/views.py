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
        return Response(status=401, data={'detail': 'You cannot delete users.'})


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (HasEventPermission, IsAuthenticated)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['Client__LastName', 'Client__Email', 'EventDate']

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Event.objects.all()
        else:
            return Event.objects.filter(SupportContact=self.request.user)

    def create(self, request, *args, **kwargs):
        used_contracts_ids = Event.objects.all().values_list('EventStatus__id', flat=True)
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            chosen_contract = ContractStatus.objects.get(
                pk=request.data['EventStatus'])
            if chosen_contract.id in used_contracts_ids:
                return Response(status=400, data={'detail': 'This contract already has an event.'})
            if chosen_contract.Signed == True:
                serializer.save(SupportContact=request.user)
                return Response(serializer.data)
            else:
                return Response(status=400, data={'Error': 'EventStatus must be True.'})
        return Response(status=400, data=serializer.errors)

    def destroy(self, request, *args, **kwargs):
        return Response(status=401, data={'detail': 'You cannot delete events.'})


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (HasClientPermission, IsAuthenticated)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['LastName', 'Email']

    def get_queryset(self):
        if self.request.user.groups.filter(name='Support'):
            assigned_clients = Event.objects.filter(
                SupportContact=self.request.user).values_list('Client__id', flat=True)
            if assigned_clients:
                return Client.objects.filter(id__in=assigned_clients)
        elif self.request.user.is_staff or self.request.user.is_superuser:
            return Client.objects.all()
        else:
            return Client.objects.filter(SalesContact=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(SalesContact=request.user)
            return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        return Response(status=401, data={'detail': 'You cannot delete clients.'})


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = (HasContractPermission, IsAuthenticated)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['Client__LastName',
                        'Client__Email', 'DateCreated',
                        'Amount']

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Contract.objects.all()
        else:
            return Contract.objects.filter(SalesContact=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = ContractSerializer(data=request.data)
        try:
            Signed = request.data['Status'] == 'true'
        except KeyError:
            Signed = False
        if serializer.is_valid():
            serializer.save(SalesContact=request.user)
            contract_status = ContractStatus.objects.create(Signed=Signed)
            contract_status.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def update(self, request, pk, *args, **kwargs):
        contract = Contract.objects.get(pk=pk)
        contract_status = ContractStatus.objects.get(pk=pk)
        serializer = ContractSerializer(contract, data=request.data)

        try:
            Signed = request.data['Status'] == 'true'
        except KeyError:
            Signed = False
        if serializer.is_valid():
            serializer.save()
            contract_status.Signed = Signed
            contract_status.save()
            return Response(serializer.data)
        else:
            return Response(status=400, data={'Error': 'Status must be True.'})

    def destroy(self, request, *args, **kwargs):
        return Response(status=401, data={'detail': 'You cannot delete contracts.'})

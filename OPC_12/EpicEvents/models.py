from django.db import models
from django.conf import settings

# Create your models here.


class Client(models.Model):
    FirstName = models.CharField(max_length=64)
    LastName = models.CharField(max_length=64)
    Email = models.EmailField(max_length=64)
    Phone = models.CharField(max_length=64)
    Mobile = models.CharField(max_length=64)
    CompanyName = models.CharField(max_length=64)
    DateCreated = models.DateTimeField(auto_now_add=True)
    DateUpdated = models.DateTimeField(auto_now=True)
    SalesContact = models.ForeignKey(
        on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL)


class Contract(models.Model):
    SalesContact = models.ForeignKey(
        on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL)
    Client = models.ForeignKey(on_delete=models.CASCADE, to=Client)
    DateCreated = models.DateTimeField(auto_now_add=True)
    DateUpdated = models.DateTimeField(auto_now=True)
    Status = models.BooleanField(default=False)
    Amount = models.FloatField()
    PaymentDue = models.DateField()


class ContractStatus(models.Model):
    signed = models.BooleanField(default=False)


class Event(models.Model):
    Client = models.ForeignKey(on_delete=models.CASCADE, to=Client)
    DateCreated = models.DateTimeField(auto_now_add=True)
    DateUpdated = models.DateTimeField(auto_now=True)
    SupportContact = models.ForeignKey(
        on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL)
    EventStatus = models.ForeignKey(
        on_delete=models.CASCADE, to=ContractStatus)
    Attendees = models.IntegerField()
    EventDate = models.DateField()
    Notes = models.TextField()

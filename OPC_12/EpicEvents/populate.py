from requests import Response
from .models import Event, Client, Contract, ContractStatus, User
import faker


def populate_clients():
    f = faker.Faker()
    for _ in range(100):
        Client.objects.create(
            FirstName=f.first_name(),
            LastName=f.last_name(),
            Email=f.email(),
            Phone=f.phone_number(),
            Mobile=f.phone_number(),
            CompanyName=f.company(),
            DateCreated=f.date_time(),
            DateUpdated=f.date_time(),
            SalesContact=User.objects.get(id=f.random_int(min=1, max=3))
        )


def populate_contracts():
    f = faker.Faker()
    for _ in range(100):
        Contract.objects.create(
            SalesContact=User.objects.get(id=f.random_int(min=1, max=3)),
            Client=Client.objects.get(id=f.random_int(min=1, max=3)),
            DateCreated=f.date_time(),
            DateUpdated=f.date_time(),
            Status=True,
            Amount=f.random_int(min=0, max=10000),
            PaymentDue=f.date_time()
        )
        ContractStatus.objects.create(
            Signed=f.boolean()
        )


def populate_events():
    f = faker.Faker()
    for _ in range(100):
        Event.objects.create(
            Client=Client.objects.get(id=f.random_int(min=1, max=3)),
            DateCreated=f.date_time(),
            DateUpdated=f.date_time(),
            SupportContact=User.objects.get(id=f.random_int(min=1, max=3)),
            EventStatus=ContractStatus.objects.get(
                id=f.random_int(min=1, max=3)),
            Attendees=f.random_int(min=0, max=1000),
            EventDate=f.date_time(),
            Notes=f.text()
        )


def populate_db(*args, **kwargs):
    populate_clients()
    populate_contracts()
    populate_events()
    print("Database populated.")
    return Response(status=200)

import random

import factory
from faker import Faker

from src.adapters.database.models import Schedule
from tests.conftest import test_sync_session_factory
from tests.factories._base import BaseFactory
from tests.factories.user_factory import UserFactory

fake = Faker()


class ScheduleFactory(BaseFactory):
    class Meta:
        model = Schedule
        sqlalchemy_session = test_sync_session_factory()

    id = factory.Sequence(lambda n: n + 1)
    user = factory.SubFactory(UserFactory)
    medicine_name = factory.LazyFunction(fake.name)
    duration_days = factory.LazyFunction(lambda: random.randint(1, 10))
    periodicity_hours = factory.LazyFunction(lambda: random.randint(1, 10))

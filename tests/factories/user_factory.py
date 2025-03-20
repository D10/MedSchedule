import factory
from faker import Faker

from src.adapters.database.models import User
from tests.conftest import test_sync_session_factory
from tests.factories._base import BaseFactory

fake = Faker()


class UserFactory(BaseFactory):
    class Meta:
        model = User
        sqlalchemy_session = test_sync_session_factory()

    id = factory.Sequence(lambda n: n + 1)
    name = factory.LazyFunction(fake.name)

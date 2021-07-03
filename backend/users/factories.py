from django.contrib.auth import get_user_model
from django.utils.text import slugify

import factory

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.PostGenerationMethodCall('set_password', 'password')

    @factory.lazy_attribute
    def username(self):
        return slugify(f'{self.first_name}_{self.last_name}')

    @factory.lazy_attribute
    def email(self):
        return f'{self.username}@example.org'

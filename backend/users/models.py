from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    subscriptions = models.ManyToManyField(
        to='self',
        related_name='subscribers',
        symmetrical=False,
        through='Subscription',
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def subscriptions_count(self):
        return self.subscriptions.count()
    subscriptions_count.short_description = 'подписок'

    def subscribers_count(self):
        return self.subscribers.count()
    subscribers_count.short_description = 'подписчиков'


class Subscription(models.Model):
    from_user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name='от пользователя',
    )
    to_user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        verbose_name='к пользователю'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('from_user', 'to_user'),
                name='subscription already exists',
            ),
            models.CheckConstraint(
                check=~Q(from_user=F('to_user')),
                name='user cannot subscribe to himself',
            ),
        ]
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'

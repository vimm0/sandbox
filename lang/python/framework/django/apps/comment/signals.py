from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.comment.models import C, A, B


@receiver(post_save, sender=A)
def generate_a(sender, instance, created, **kwargs):
    print('called from signal a')


@receiver(post_save, sender=B)
def generate_b(sender, instance, created, **kwargs):
    print('called from signal b')


@receiver(post_save, sender=C)
def generate_c(sender, instance, created, **kwargs):
    print('called from signal c')

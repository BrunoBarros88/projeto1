import os

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from receitas.models import Receita


def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        ...


@receiver(pre_delete, sender=Receita)
def recipe_cover_delete(sender, instance, *args, **kwargs):
    old_instance = Receita.objects.get(pk=instance.pk)

    if old_instance:
        delete_cover(old_instance)


@receiver(pre_save, sender=Receita)
def recipe_cover_update(sender, instance, *args, **kwargs):

    try:
        old_instance = Receita.objects.get(pk=instance.pk)
    except Receita.DoesNotExist:
        return

    is_new_cover = old_instance.cover != instance.cover

    if is_new_cover:
        delete_cover(old_instance)

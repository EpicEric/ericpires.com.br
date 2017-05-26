from django.db import models
from telegrambot.models import Chat


class Language(models.Model):
    name = models.CharField(
        max_length=64,
    )
    shortname = models.CharField(
        max_length=64,
    )
    value = models.PositiveIntegerField(
        unique=True,
    )
    default_code = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Code(models.Model):
    chat = models.OneToOneField(
        Chat,
        on_delete=models.CASCADE,
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
    )
    code = models.TextField(blank=True)
    stdin = models.TextField(blank=True)

    def __str__(self):
        return self.chat.__str__()

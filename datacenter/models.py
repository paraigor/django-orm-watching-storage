from datetime import timedelta

from django.db import models
from django.utils import timezone


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f"{self.owner_name} (inactive)"


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f"leaved at {self.leaved_at}"
                if self.leaved_at
                else "not leaved"
            ),
        )

    def get_duration(self):
        enter_time = timezone.localtime(value=self.entered_at)
        exit_time = timezone.localtime(value=self.leaved_at)
        return exit_time - enter_time

    def is_long(self, minutes=60):
        enter_time = timezone.localtime(value=self.entered_at)
        exit_time = timezone.localtime(value=self.leaved_at)
        delta = exit_time - enter_time
        return delta / timedelta(minutes=minutes) > 1

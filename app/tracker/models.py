from django.conf import settings
from django.db import models
from django.utils import timezone


class ConsumptionEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='consumption_entries')
    name = models.CharField(max_length=255, blank=True, null=True)
    calories = models.IntegerField()
    date = models.DateField(default=timezone.localdate)
    quantity_g = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-date', '-id']
        indexes = [
            models.Index(fields=['user', 'date']),
        ]

    def __str__(self):
        base = f"{self.calories} kcal"
        if self.name:
            return f"{self.name} - {base}"
        return base


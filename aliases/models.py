from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings

class Alias(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='lessons',
                             verbose_name='user', help_text='Set user')

    approved = models.BooleanField(default=False, verbose_name='Approved')
    last_name = models.CharField(max_length=256, verbose_name='Last name')
    first_name = models.CharField(max_length=256, verbose_name='First name')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    def clean(self):
        if self.user.first_name == self.first_name and self.user.last_name == self.last_name:
            raise ValidationError(message='ALIAS_VALIDATION_NAMES')

    def str(self):
        return f'Alias by {self.user.full_name}'

    class Meta:
        db_table = 'aliases'
        verbose_name = 'Alias'
        verbose_name_plural = 'Aliases'
        ordering = ('approved',)
        unique_together = (
            ('user', 'last_name', 'first_name'),
        )
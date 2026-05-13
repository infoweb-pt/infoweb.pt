from django.db import models


class LostCustomerLead(models.Model):
    email = models.EmailField()
    weekly_loss = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_loss = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lost Customer Lead'
        verbose_name_plural = 'Lost Customer Leads'

    def __str__(self):
        return f'{self.email} — €{self.monthly_loss}/mo ({self.created_at:%Y-%m-%d})'


class PresenceScoreLead(models.Model):
    email = models.EmailField()
    score = models.PositiveSmallIntegerField()
    answers = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Presence Score Lead'
        verbose_name_plural = 'Presence Score Leads'

    def __str__(self):
        return f'{self.email} — score {self.score}/100 ({self.created_at:%Y-%m-%d})'


class ToolContactLead(models.Model):
    """Optional email capture from free-tool CTAs (e.g. WhatsApp QR generator)."""

    email = models.EmailField()
    source = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Tool Contact Lead'
        verbose_name_plural = 'Tool Contact Leads'

    def __str__(self):
        return f'{self.email} — {self.source} ({self.created_at:%Y-%m-%d})'

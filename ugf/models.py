from django.db import models

# hopefully things are passed in like this
ROUND_TYPES = (
    ("Seed", "seed"),
    ("Pre-Series A", "pre-series-a"),
    ("Series A", "a"),
    ("Series B", "b"),
    ("Series C", "c"),
    ("Series D", "d"),
    ("Exited (acquired)", "acquired"),
    ("Exited (IPO)", "ipo"),
    ("Series E", "e"),
    ("Series F", "f"),
    ("Series G", "g"),
    ("Series H", "h"),
    ("Series J", "j"),
    ("Series I", "i"),
    ("Series I", "i"),
)

class Company(models.Model):
    """Model definition for Company."""

    name = models.CharField(max_length=255)
    retrieved_name = models.CharField(null=True, blank=True, max_length=255)

    source = models.ForeignKey("Source", null=True, blank=True)

    # standardize how things are passed in: Series A -> a, Series b -> b, Exited (ipo) -> ipo, etc
    current_series = models.CharField(null=True, blank=True, max_length=255)
    last_funding_date = models.DateTimeField(null=True, blank=True)
    last_funding_amount = models.BigIntegerField(default=0.0)
    total_funding = models.BigIntegerField(default=0.0)

    date_created = models.DateTimeField(auto_now_add=True)

    valid_candidate = models.BooleanField(default=True)
    data_retrieved = models.BooleanField(default=False)
    date_data_retrieved = models.DateTimeField(null=True, blank=True)

    # should we get mattermark / growth score? Could be interesting way to measure these

    class Meta:
        """Meta definition for Company."""
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __unicode__(self):
        """Unicode representation of Company."""
        return self.name

    def get_last_funded_date(self):
        return self.last_funding_date


class Source(models.Model):
    """Model definition for Source."""

    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for Source."""

        verbose_name = 'Source'
        verbose_name_plural = 'Sources'

    def __unicode__(self):
        """Unicode representation of Source."""
        return self.name

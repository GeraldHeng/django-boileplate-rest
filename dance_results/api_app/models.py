from django.db import models
from django.conf import settings
from datetime import datetime


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Employee(TimeStampMixin):
    eno = models.IntegerField()
    ename = models.CharField(max_length=200)
    esalary = models.FloatField()
    eaddr = models.CharField(max_length=200)

    def __str__(self):
        return self.ename


class Competition(TimeStampMixin):
    title = models.CharField(max_length=200)
    description = models.TextField()
    venue = models.TextField()
    email = models.EmailField()
    logo_path = models.URLField()
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    publish_status = models.BooleanField(default=False)

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="creator", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


COUNTRY_CODES = (
    ("SG", "singapore"),
    ("MY", "malaysia"),
    ("KR", "korea"),
)


class Adjudicator(TimeStampMixin):
    name = models.CharField(max_length=200)
    description = models.TextField()
    country_code = models.CharField(max_length=100, choices=COUNTRY_CODES)
    competition = models.ForeignKey(
        Competition, related_name="adjudicators", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Dance(TimeStampMixin):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


class Event(TimeStampMixin):
    title = models.CharField(max_length=200)
    description = models.TextField()
    competition = models.ForeignKey(
        Competition, related_name="events", on_delete=models.CASCADE)
    dances = models.ManyToManyField(Dance, related_name='events',)

    def __str__(self):
        return self.title

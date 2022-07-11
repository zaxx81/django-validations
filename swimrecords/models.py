from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models


def relay_check(relay):
    options = ['True', 'False']
    if relay not in options:
        raise ValidationError("'None' value must be either True or False.")

def stroke_check(stroke):
    options = ['front crawl', 'butterfly', 'breast', 'back', 'freestyle']
    if stroke not in options:
        raise ValidationError(f"{stroke} is not a valid stroke")
    
def distance_check(distance):
    limit = 50
    if distance <= limit:
        raise ValidationError(f"Ensure this value is greater than or equal to {limit}.")
    
def record_date_check(record_date):
    now = timezone.now()
    if record_date > now:
        raise ValidationError("Can't set record in the future.")
    
class SwimRecord(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    team_name = models.CharField(max_length=255)
    relay = models.BooleanField(default=False, validators=[relay_check])
    stroke = models.CharField(max_length=255, validators=[stroke_check])
    distance = models.IntegerField(validators=[distance_check])
    record_date = models.DateTimeField(validators=[record_date_check])
    record_broken_date = models.DateTimeField()

    def clean(self):
        if self.record_broken_date != None and self.record_date != None:
            if self.record_broken_date < self.record_date:
                raise ValidationError({'record_broken_date': ["Can't break record before record was set."]})
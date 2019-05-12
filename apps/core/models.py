from django.db import models


class TimeStampObject(models.Model):
    """
    Mixin for time specific auto fields (DRY)
    """
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

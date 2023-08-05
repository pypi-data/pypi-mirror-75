from django.db import models

from cms.models import CMSPlugin
from filer.fields.image import FilerImageField
from mixins.models import URLMixin


class PageCardBlock(CMSPlugin):
    """
    Model for the page card block plugin
    """

    pass


class PageCard(CMSPlugin, URLMixin):
    """
    A model for an individual page card
    """

    title = models.CharField(max_length=256)
    summary = models.CharField(max_length=140, help_text="Limited to 140 characters")
    image = FilerImageField(related_name="+", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """
        String representation of the object
        """
        return f"Page Card #{self.pk}"

from django.db import models

from cms.models import CMSPlugin
from filer.fields.image import FilerImageField
from mixins.models import YoutubeURLMixin


class ContentWidthVideo(CMSPlugin, YoutubeURLMixin):
    """
    Represents a content width video object
    """

    image = FilerImageField(related_name="+", on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=128, blank=True)
    alt_title = models.CharField(max_length=128, blank=True, default=title)

    def __str__(self):
        """
        String representation of the object
        """
        return f"Content Width Video {self.pk}"

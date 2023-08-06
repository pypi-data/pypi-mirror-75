from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from . import models

__all__ = ["HeroImagePlugin"]


@plugin_pool.register_plugin
class HeroImagePlugin(CMSPluginBase):
    """
    CMS plugin for the Image Hero model
    """

    model = models.HeroImage
    name = "Image Hero"
    render_template = "plugins/hero_image.html"

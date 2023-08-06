from cms.plugin_pool import CMSPluginBase, plugin_pool

from . import models

__all__ = ["ContentWidthImagePlugin"]


@plugin_pool.register_plugin
class ContentWidthImagePlugin(CMSPluginBase):
    """
    Image plugin
    """

    name = "Content Width Image"
    model = models.ContentWidthImage
    render_template = "plugins/content_width_image.html"

from cms.plugin_pool import CMSPluginBase, plugin_pool

from . import models

__all__ = ["ContentWidthVideoPlugin"]


@plugin_pool.register_plugin
class ContentWidthVideoPlugin(CMSPluginBase):
    """
    Content width video plugin
    """

    name = "Content Width Video"
    model = models.ContentWidthVideo
    render_template = "plugins/content_width_video.html"

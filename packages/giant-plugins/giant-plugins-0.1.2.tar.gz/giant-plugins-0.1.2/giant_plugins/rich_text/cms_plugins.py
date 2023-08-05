from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from . import models

__all__ = ["RichTextPlugin"]


@plugin_pool.register_plugin
class RichTextPlugin(CMSPluginBase):
    """
    Rich text plugin
    """

    name = "Rich Text"
    model = models.RichText
    render_template = "plugins/rich_text.html"

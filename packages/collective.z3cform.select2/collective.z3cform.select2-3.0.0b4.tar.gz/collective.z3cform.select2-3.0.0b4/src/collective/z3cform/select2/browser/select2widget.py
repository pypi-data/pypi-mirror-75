# -*- coding: utf-8 -*-
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.select.widget import Widget as SelectWidget
from eea.facetednavigation.widgets.select.interfaces import ISelectSchema

from eea.faceted.vocabularies.utils import lowercase_text

from zope.i18n import MessageFactory

_ = MessageFactory('collective.z3cform.select2')


class ISelect2Schema(ISelectSchema):
    """ """


class Widget(SelectWidget):
    """ Widget
    """

    # Widget properties
    widget_type = 'select2'
    widget_label = _('Select2')

    index = ViewPageTemplateFile('templates/select2.pt')

    @property
    def default(self):
        """ Get default values
        """
        default = super(SelectWidget, self).default
        if not default:
            return []

        if isinstance(default, (str, unicode)):
            default = [default, ]

        return default

    def selected(self, key):
        """ Return True if key in self.default
        """
        default = self.default
        if not default:
            return False

        for item in default:
            if lowercase_text(key, item) == 0:
                return True

        return False

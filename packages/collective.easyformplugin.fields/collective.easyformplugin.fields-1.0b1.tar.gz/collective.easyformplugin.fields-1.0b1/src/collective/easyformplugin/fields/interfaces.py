# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from collective.easyform.interfaces import IEasyFormLayer
from collective.easyformplugin.fields import _
from plone import api
from plone.app.textfield import RichText
from zope.i18n import translate
from zope.interface import provider
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema.interfaces import IContextAwareDefaultFactory

import z3c.form.interfaces
import zope.schema.interfaces


@provider(IContextAwareDefaultFactory)
def default_checkbox_label(context):
    return translate(
        _("consent_checkbox_label__default", default=u"Yes, I agree"),
        target_language=api.portal.get_current_language(),
    )


class IBrowserLayer(IEasyFormLayer):
    """Marker interface that defines a browser layer."""


class IConsent(zope.schema.interfaces.IBool):
    rich_label = RichText(
        title=_("consent_rich_label__label", default=u"Rich Label"),
        description=_(
            "consent_rich_label__help",
            default=u"A text that will appear above the checkbox to explain the nature of the consent.",
        ),
        default=u"",
        required=False,
        missing_value=u"",
    )
    checkbox_label = zope.schema.TextLine(
        title=_("consent_checkbox_label__label", default=u"Checkbox Label"),
        description=_(
            "consent_checkbox_label__help",
            default=u"A text that will be displayed next to the checkbox, e.g. 'Yes, I agree'.",
        ),
        # defaultFactory=default_checkbox_label,  # the default's value is apparently not stored. TODO: revisit lated.
        default=u"",
        required=False,
        missing_value=u"",
    )


class IConsentWidget(z3c.form.interfaces.ISingleCheckBoxWidget):
    """ Consent Widget. """


class IDivider(zope.schema.interfaces.IField):
    """ Similar to a label, different display."""


class IDividerWidget(z3c.form.interfaces.IWidget):
    """ Divider Widget."""

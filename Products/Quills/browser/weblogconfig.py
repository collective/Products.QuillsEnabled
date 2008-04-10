# Zope imports
from zope.interface import implements
from zope.formlib import form

# plone imports
from Products.statusmessages.interfaces import IStatusMessage

# Quills imports
from quills.core.browser.weblogconfig import WeblogConfigEditForm
from quills.core.browser.weblogconfig import WeblogConfigAnnotations
from quills.app.interfaces import IWeblogEnhancedConfiguration
from quills.app.browser.weblogconfig import StateAwareWeblogConfig


class WeblogEnhancedConfig(StateAwareWeblogConfig):
    """
    >>> from zope.interface.verify import verifyClass
    >>> verifyClass(IWeblogEnhancedConfiguration, WeblogEnhancedConfig)
    True
    """

    implements(IWeblogEnhancedConfiguration)

    def _get_defaultType(self):
        return self._config.get('default_type', 'Document')
    def _set_defaultType(self, value):
        self._config['default_type'] = value
    default_type = property(_get_defaultType, _set_defaultType)


class WeblogEnhancedConfigEditForm(WeblogConfigEditForm):
    """Edit form for weblog view configuration.
    """

    form_fields = form.Fields(IWeblogEnhancedConfiguration)
    label = u'Weblog View Configuration'

    def setUpWidgets(self, ignore_request=False):
        self.adapters = {}
        wvconfig = IWeblogEnhancedConfiguration(self.context)
        self.widgets = form.setUpEditWidgets(
            self.form_fields, self.prefix, wvconfig, self.request,
            adapters=self.adapters, ignore_request=ignore_request
            )

    @form.action("submit")
    def submit(self, action, data):
        """
        """
        wvconfig = IWeblogEnhancedConfiguration(self.context)
        form.applyChanges(wvconfig, self.form_fields, data)
        msg = 'Configuration saved.'
        IStatusMessage(self.request).addStatusMessage(msg, type='info')

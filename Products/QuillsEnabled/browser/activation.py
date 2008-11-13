# zope imports
from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from zope import event

# quills imports
from quills.core.interfaces.enabled import IPossibleWeblog
from quills.core.interfaces.enabled import IWeblogEnhanced

# Local imports
from Products.QuillsEnabled.activation import WeblogActivationEvent, WeblogDeactivationEvent


class BlogActivation(object):
    """ This view determines if it's possible to activate or
        deactivate the blog features on the folder.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def can_activate(self):
        return IPossibleWeblog.providedBy(self.context) and \
               not IWeblogEnhanced.providedBy(self.context)

    def can_deactivate(self):
        return IWeblogEnhanced.providedBy(self.context)


class Toggle(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        if IWeblogEnhanced.providedBy(self.context):
            # deactivate blog
            event.notify(WeblogDeactivationEvent(self.context))
            noLongerProvides(self.context, IWeblogEnhanced)
            msg = 'blog deactivated'
        elif IPossibleWeblog.providedBy(self.context):
            alsoProvides(self.context, IWeblogEnhanced)
            event.notify(WeblogActivationEvent(self.context))
            msg = 'blog activated'
        else:
            msg = 'not bloggable'
        # XXX This should set the status message with something like:
        # from Products.statusmessages.interfaces import IStatusMessage
        # IStatusMessage(self.request).addStatusMessage(msg, type='info')
        url = self.context.absolute_url() + '?portal_status_message=' + msg
        self.request.response.redirect(url)

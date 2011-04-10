# Zope imports
from zope.interface import implements

# Quills imports
from quills.core.interfaces import IWeblog
from quills.core.interfaces import IWeblogEntry
from quills.core.browser.interfaces import IWeblogView
from quills.core.browser.interfaces import IWeblogEntryView
from quills.core.browser.interfaces import ITopicView
from quills.app.browser.weblogview import WeblogView as BaseWeblogView
from quills.app.browser.weblogview import WeblogEntryView as BaseWeblogEntryView
from quills.app.interfaces import IWeblogEnhancedConfiguration


class BaseView:
    pass


class WeblogView(BaseWeblogView, BaseView):
    """A class with helper methods for use in views/templates.
    """

    implements(IWeblogView)

    def getWeblog(self):
        return IWeblog(self.context)

    def getWeblogContentObject(self):
        return self.context

    def getConfig(self):
        """See IWeblogView.
        """
        return IWeblogEnhancedConfiguration(self.context)


class WeblogEntryView(BaseWeblogEntryView, BaseView):
    """
    """
    implements(IWeblogEntryView)

    def getWeblog(self):
        return self.getWeblogEntry().getWeblog()

    def getWeblogContentObject(self):
        return self.getWeblogEntry().getWeblogContentObject()

    def getConfig(self):
        """See IWeblogView.
        """
        obj = self.getWeblogContentObject()
        return IWeblogEnhancedConfiguration(obj)

    def getWeblogEntry(self):
        """See IWeblogEntryView.
        """
        return IWeblogEntry(self.context).__of__(self.context)
    

class TopicView(WeblogView):
    """
    """
    implements(ITopicView)

    def getLastModified(self):
        """See ITopic.
        """
        weblog = self.getParentWeblog()
        entries = weblog.getEntries()
        if entries:
            # XXX modified should be something in an interface
            return entries[0].modified

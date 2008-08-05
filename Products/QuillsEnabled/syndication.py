# Zope 3 imports
from zope.interface import implements
from zope.component import getMultiAdapter

# Zope 2 imports
from DateTime.DateTime import DateTime

# CMF imports
from Products.CMFCore.utils import getToolByName

from Products.fatsyndication.adapters import BaseFeed
from Products.fatsyndication.adapters import BaseFeedSource
from Products.fatsyndication.adapters import BaseFeedEntry
from Products.basesyndication.interfaces import IFeedSource
from Products.basesyndication.interfaces import IFeedEntry
from quills.core.interfaces import IWeblog, IWeblogEntry

class WeblogFeed(BaseFeed):
    """Adapter from Quills Weblog instances to IFeed
    """

    def getModifiedDate(self):
        """See IFeed.
        """
        
        # Quills has the luxury of being able to compute the effective modification date
        # in a much more efficient manner, i.e. by querying the catalog:
        path = '/'.join(self.context.getPhysicalPath())
        results = self.context.portal_catalog(
            meta_type=['WeblogEntry', 'Discussion Item',],
            path={'query':path, 'level': 0},
            sort_on = 'modified',
            sort_order = 'reverse',
            review_state = 'published')

        # just like fatsyndication, we return 'now', if there
        # aren't any entries:
        try:
            return results[0].getObject().modified()
        except IndexError:
            return DateTime()
             


class WeblogFeedSource(BaseFeedSource):
    """Adapter from Quills Weblog instances to IFeedSource
    """

    implements(IFeedSource)
    def __init__(self, context):
        self.context = IWeblog(context)

    def getFeedEntries(self, max_only=True):
        """See IFeedSoure
        """
        if max_only:
            num_of_entries = self.getMaxEntries()
        else:
            num_of_entries = 0 # signals to fetch _all_ items
        brains = self.context.getEntries(num_of_entries)
        return [IFeedEntry(brain.getObject()) for brain in brains]

    # Quills always returns sorted entries, so we can override fatsyndications
    # expensive (but generic) implementation:
    getSortedFeedEntries = getFeedEntries


class TopicFeed(BaseFeed):
    pass


class TopicFeedSource(BaseFeedSource):
    """Adapter from Quills Topic instances to IFeedSource
    """

    implements(IFeedSource)
    def __init__(self, context):
        self.context = IWeblog(context)

    def getFeedEntries(self):
        """See IFeedSoure
        """
        brains = self.context.getEntries()
        return [IFeedEntry(brain.getObject()) for brain in brains]


class WeblogEntryFeed(BaseFeed):
    pass


class WeblogEntryFeedSource(BaseFeedSource):
    """An adapter from IWeblogEntry to IFeedSource that feeds out the
    entry's comments.
    """

    implements(IFeedSource)

    def getFeedEntries(self):
        """See IFeedSource
        """
        d_tool = getToolByName(self.context, 'portal_discussion')
        discussion = d_tool.getDiscussionFor(self.context)
        replies = [IFeedEntry(reply) for reply in discussion.getReplies()]
        return [IFeedEntry(self.context)] + replies


class WeblogEntryFeedEntry(BaseFeedEntry):
    """
    """

    implements(IFeedEntry)
    def __init__(self, context):
        self.context = IWeblogEntry(context)
    
    def getXhtml(self):
        html_types = ('text/html', 'text/x-rst',
                      'text/restructured', 'text/structured')
        if self.context.text.mimetype in html_types:
            return self.context.getText()
        else:
            return None

    def getWebURL(self):
        """See IFeedEntry.
        """
        we_view = getMultiAdapter((self.context, self.context.REQUEST),
                                  name='weblogentry_view')
        return we_view.getArchiveURLFor(self.context)

    def getBody(self):
        """See IFeedEntry.
        """
        return self.context.getText()

    def getModifiedDate(self):
        """See IFeedEntry.
        """

        # we override fatsyndications generic implementation and compare the 
        # entry's modification date with those of any comments:
        modified = self.context.modified()

        path = '/'.join(self.context.getPhysicalPath())
        results = self.context.portal_catalog(
            meta_type=['Discussion Item',],
            path={'query':path, 'level': 0},
            sort_on = 'modified',
            sort_order = 'reverse',
            review_state = 'published')

        try:
            comment_mod = results[0].getObject().modified()
            if comment_mod > modified:
                modified = comment_mod
        except IndexError:
             pass
        return modified

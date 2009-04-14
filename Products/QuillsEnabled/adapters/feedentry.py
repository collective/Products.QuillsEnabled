from zope.interface import implements
from zope.component import getMultiAdapter
from Products.basesyndication.interfaces import IFeedEntry
from Products.fatsyndication.adapters.feedentry import DocumentFeedEntry
from Products.Archetypes.config import UUID_ATTR, REFERENCE_CATALOG
from Products.CMFCore.utils import getToolByName
from quills.core.interfaces import IWeblogEntry
from quills.app.interfaces import IWeblogEnhancedConfiguration


class WeblogEntryFeedEntry(DocumentFeedEntry):
    """Adapter from IPossibleWeblogEntry to IFeedEntry."""

    implements(IFeedEntry)

    def getWebURL(self):
        """Overridden to return the archvie url"""
        we_view = getMultiAdapter((self.context, self.context.REQUEST),
                                  name='weblogentry_view')
        entry = IWeblogEntry(self.context).__of__(self.context)
        return we_view.getArchiveURLFor(entry)

    def getModifiedDate(self):
        """See IFeedEntry.
        """

        # we override fatsyndications generic implementation and compare the 
        # entry's modification date with those of any comments:
        modified = self.context.modified()

        path = '/'.join(self.context.getPhysicalPath())
        weblog_config = IWeblogEnhancedConfiguration(self.context.aq_inner.aq_parent)
        results = self.context.portal_catalog(
            meta_type=['Discussion Item',],
            path={'query':path, 'level': 0},
            sort_on = 'modified',
            sort_order = 'reverse',
            review_state = weblog_config.published_states)

        try:
            comment_mod = results[0].getObject().modified()
            if comment_mod > modified:
                modified = comment_mod
        except IndexError:
             pass
        return modified


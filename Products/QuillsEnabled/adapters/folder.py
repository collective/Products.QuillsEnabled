# Zope imports
from zope.interface import implements
from zope.component.interface import interfaceToName
from zope.component import getUtility
from zope.app.container.interfaces import INameChooser
from Products.ZCatalog.CatalogBrains import AbstractCatalogBrain
from DateTime import DateTime

# Plone imports
from Products.CMFCore.utils import getToolByName
from plone.i18n.normalizer.interfaces import IIDNormalizer

# Quills imports
from quills.core.interfaces import IWeblog
from quills.core.interfaces import IWeblogEntry
from quills.core.interfaces import ITopic
from quills.core.interfaces import IWeblogEntry
from quills.core.interfaces import IPossibleWeblogEntry
from quills.app.topic import Topic
from quills.app.topic import AuthorTopic
from quills.app.topic import TopicContainer
from quills.app.archive import ArchiveContainer
from quills.app.archive import YearArchive
from quills.app.weblogentrybrain import WeblogEntryCatalogBrain
from quills.app.weblog import WeblogMixin
from quills.app.interfaces import IWeblogEnhancedConfiguration


class Folder2Weblog(WeblogMixin):
    """Adapts an ATFolder to IWeblog.

    >>> from zope.interface.verify import verifyClass
    >>> verifyClass(IWeblog, Folder2Weblog)
    True
    """

    implements(IWeblog)

    def __init__(self, context):
        self.context = context
        self._portal = None
        self._catalog = None

    def hasEntry(self, id):
        return self.context.hasObject(id)

    def getEntry(self, id):
        """See IWeblog.
        """
        if self.context.hasObject(id):
            obj = getattr(self.context, id)
            return IWeblogEntry(obj)
        return None

    def getEntries(self, maximum=None, offset=0):
        """See IWeblog.
        """
        catalog, portal = self._setCatalog()
        catalog._catalog.useBrains(WeblogEntryCatalogBrain)
        weblog_config = IWeblogEnhancedConfiguration(self.context)
        results = catalog(
            object_provides=interfaceToName(portal, IPossibleWeblogEntry),
            path={ 'query' : '/'.join(self.context.getPhysicalPath()),
                   'level' : 0, },
            effective={'query' : DateTime(), 'range' : 'max'},
            sort_on='effective',
            sort_order='reverse',
            review_state={ 'query'    : weblog_config.published_states,
                           'operator' : 'or'})
        return self._filter(results, maximum, offset)

    def getArchives(self):
        """See IWeblog.
        """
        return ArchiveContainer('archive').__of__(self.context)

    def getTopics(self):
        """See IWeblog.
        """
        topic_container = TopicContainer('topics').__of__(self.context)
        return topic_container.getTopics()

    def getTopicById(self, id):
        """See IWeblog.
        """
        topic_container = TopicContainer('topics').__of__(self.context)
        return topic_container.getTopicById(id)

    def getAuthors(self):
        """See IWeblog.
        """
        catalog, portal = self._setCatalog()
        results = catalog(
            object_provides=interfaceToName(portal, IPossibleWeblogEntry),
            path={ 'query' : '/'.join(self.context.getPhysicalPath()),
                   'level' : 0, },
            review_state='published')
        authors = {}
        for brain in results:
            authors[brain.Creator] = None
        return [AuthorTopic(author).__of__(self.context) for author in authors.keys()]

    def getAuthorById(self, id):
        """See IWeblog.
        """
        return AuthorTopic(id).__of__(self)

    def getSubArchives(self):
        """See IWeblogArchive.
        """
        config = IWeblogEnhancedConfiguration(self.context)
        archive_id = config.archive_format
        arch_container = ArchiveContainer(archive_id).__of__(self.context)
        if archive_id:
            # If there is an extra archive URL segment needed, then we inject
            # the ArchiveContainer into the acquisition chain for the returned
            # sub-archives
            return arch_container.getSubArchives()
        # Otherwise, we'll just use the ArchiveContainer's _getEntryYears
        # implementation to figure out what YearArchive objects to return
        # directly in the context of this IWeblog.
        years = arch_container._getEntryYears()
        return [YearArchive(year).__of__(self.context) for year in years]

    def addEntry(self,
                 title,
                 excerpt,
                 text,
                 topics=[],
                 id=None,
                 pubdate=None,
                 mimetype=None):
        """Add an entry from the provided arguments.  If id is None, normalize
        the title to create an id.  If pubdate is None, ignore it.
        Return the new entry.
        """
        config = IWeblogEnhancedConfiguration(self.context)
        if id is None:
            id = getUtility(IIDNormalizer).normalize(title)
        self.context.invokeFactory(id=id, type_name=config.default_type)
        obj = getattr(self.context, id)
        entry = IWeblogEntry(obj)
        entry.setTitle(title)
        entry.setText(text, mimetype)
        entry.setExcerpt(excerpt)
        if topics:
            entry.setTopics(topics)
        if pubdate is not None:
            entry.setPublicationDate(pubdate)
        #obj.reindexObject()
        return entry

    def addFile(self, content, mimetype, id=None, title=''):
        """See IWeblog.
        """
        id = self._genUniqueId(self.context, id, title)
        portal_type = self._getPortalTypeForMimeType(mimetype)
        self.context.invokeFactory(id=id,
                                   type_name=portal_type,
                                   title=title,
                                   file=content)
        return self.context[id]

    def getDrafts(self, maximum=None, offset=0):
        """See IWeblog.
        """
        catalog, portal = self._setCatalog(WeblogEntryCatalogBrain)
        weblog_config = IWeblogEnhancedConfiguration(self.context)
        results = catalog(
            object_provides=interfaceToName(portal, IPossibleWeblogEntry),
            path={ 'query' : '/'.join(self.context.getPhysicalPath()),
                   'level': 0, },
            sort_on='effective',
            sort_order='reverse',
            review_state={ 'query'    : weblog_config.draft_states,
                           'operator' : 'or'})
        return self._filter(results, maximum, offset)

    def getAllEntries(self, maximum=None, offset=0):
        """See IWeblog.
        """
        catalog, portal = self._setCatalog()
        catalog._catalog.useBrains(WeblogEntryCatalogBrain)
        results = catalog(
            object_provides=interfaceToName(portal, IPossibleWeblogEntry),
            path={ 'query' : '/'.join(self.context.getPhysicalPath()),
                   'level' : 0, },
            sort_on = 'effective',
            sort_order = 'reverse')
        return self._filter(results, maximum, offset)

    def __len__(self):
        return len(self.getEntries())

    def deleteEntry(self, entry_id):
        """See IWeblog.
        """
        self.context.manage_delObjects(ids=[entry_id])

    def _setCatalog(self, brains=None):
        if self._catalog is None:
            self._catalog = getToolByName(self.context, 'portal_catalog')
        catalog = self._catalog
        if brains is None:
            catalog._catalog.useBrains(AbstractCatalogBrain)
        else:
            catalog._catalog.useBrains(brains)
        if self._portal is None:
            self._portal = getToolByName(self.context, 'portal_url').getPortalObject()
        portal = self._portal
        return catalog, portal

    def getWeblogContentObject(self):
        """See IWeblog.
        """
        return self.context

    def getWeblog(self):
        """See IWeblog.
        """
        return self

# Standard library imports
from datetime import datetime

# Zope imports
from zope.interface import implements
from DateTime.DateTime import DateTime
from Acquisition import Explicit

# Plone imports
from Products.CMFCore.utils import getToolByName

# Quills imports
from quills.core.interfaces import IWorkflowedWeblogEntry
from quills.app.topic import Topic, AuthorTopic
from quills.app.utilities import QuillsMixin, recurseToInterface
from quills.core.interfaces import IWeblog, IWeblogEnhanced


class Document2WeblogEntry(Explicit, QuillsMixin):
    """Adapts an ATDocument to IWeblogEntry.

    >>> from zope.interface.verify import verifyClass
    >>> verifyClass(IWorkflowedWeblogEntry, Document2WeblogEntry)
    True
    """

    implements(IWorkflowedWeblogEntry)

    # XXX Awful hack!
    #__allow_access_to_unprotected_subobjects__ = True

    def __init__(self, context):
        self.context = context

    def getId(self):
        """See IWeblogEntry.
        """
        return self.context.getId()

    def getTitle(self):
        """See IWeblogEntry.
        """
        return self.context.Title()

    def setTitle(self, title):
        """See IWeblogEntry.
        """
        self.context.setTitle(title)

    def getText(self):
        """See IWeblogEntry.
        """
        return self.context.getText()

    def getMimeType(self):
        """See IWeblogEntry.
        """
        # (ATCT handles the mechanics for determining the default for us)
        return self.context.getField('text').getContentType(self.context)

    def setText(self, text, mimetype=None):
        """See IWeblogEntry.
        """
        # if no mimetype was specified, we use the default
        if mimetype is None:
            mimetype = self.getMimeType()
        self.context.getField('text').set(self.context, text, mimetype=mimetype)

    def getTopics(self):
        """See IWeblogEntry.
        """
        weblog = self.getWeblogContentObject()
        keywords = self.context.Subject()
        return [Topic(kw).__of__(weblog) for kw in keywords]

    def getAuthors(self):
        """See IWeblogEntry.
        """
        weblog = self.getWeblogContentObject()
        creators = self.context.Creators()
        return [AuthorTopic(each).__of__(weblog) for each in creators]

    def getExcerpt(self):
        """See IWeblogEntry.
        """
        return self.context.Description()

    def setExcerpt(self, excerpt):
        """See IWeblogEntry.
        """
        self.context.setDescription(excerpt)

    def setTopics(self, topic_ids):
        """See IWeblogEntry.
        """
        self.context.setSubject(topic_ids)

    def edit(self, title, excerpt, text, topics, mimetype=None):
        """See IWeblogEntry.
        """
        # if no mimetype was specified, we use the default
        if mimetype is None:
            mimetype = self.getMimeType()
        self.setText(text, mimetype=mimetype)
        self.setTitle(title)
        self.setExcerpt(excerpt)
        if topics:
            self.setTopics(topics)
        else:
            self.setTopics([])
        self.context.reindexObject()

    def getPublicationDate(self):
        """See IWeblogEntry.
        """
        return self.context.getEffectiveDate()

    def setPublicationDate(self, datetime):
        """See IWeblogEntry.
        """
        self.context.setEffectiveDate(datetime)

    def publish(self, pubdate=None):
        """See IWorkflowedWeblogEntry.
        """
        if self.isPublished():
            # do nothing if the entry has already been published
            return
        # XXX Need to be able to handle python datetime instances for pubdate.
        if pubdate is None:
            pubdate = DateTime()
        self.setPublicationDate(pubdate)

        wf_tool = getToolByName(self.context, 'portal_workflow')
        try:
            wf_tool.doActionFor(self.context, 'publish')
        except WorkflowException:
            state = wf_tool.getInfoFor(self.context, 'review_state')
            workflow = wf_tool.getWorkflowsFor(self.context)[0].id
            objectPath = "/".join(self.context.getPhysicalPath())
            log("WeblogEntry.publish failed, most probable because the current "
                "state '%s' of workflow '%s' of entry '%s' does not define a "
                "transition 'publish'. To solve this either use another "
                "workflow, adapt the workflow, or restrain from using this "
                "method for now. Sorry." % (state, workflow, objectPath))
            raise
        self.context.reindexObject()

    def retract(self):
        """See IWorkflowedWeblogEntry.
        """
        if not self.isPublished():
            # do nothing if the entry has already been published
            return
        wf_tool = getToolByName(self.context, 'portal_workflow')
        try:
            wf_tool.doActionFor(self.context, 'retract')
        except WorkflowException:
            state = wf_tool.getInfoFor(self.context, 'review_state')
            workflow = wf_tool.getWorkflowsFor(self.context)[0].id
            objectPath = "/".join(self.context.getPhysicalPath())
            log("WeblogEntry.retract failed, most probable because the current "
                "state '%s' of workflow '%s' of entry '%s' does not define a "
                "transition 'retract'. To solve this either use another "
                "workflow, adapt the workflow, or restrain from using this "
                "method for now. Sorry." % (state, workflow, objectPath))
            raise
        self.setPublicationDate(None)
        self.context.reindexObject()


    def isPublished(self):
        """See IWorkflowedWeblogEntry.
        """
        wf_tool = getToolByName(self.context, 'portal_workflow')
        review_state = wf_tool.getInfoFor(self.context, 'review_state')
        if review_state == 'published':
            return True
        return False

    def getWeblogContentObject(self):
        """See IWeblogEntry.
        """
        return recurseToInterface(self.context, (IWeblog, IWeblogEnhanced))

    def getWeblogEntryContentObject(self):
        """See IWeblogEntry.
        """
        return self.context


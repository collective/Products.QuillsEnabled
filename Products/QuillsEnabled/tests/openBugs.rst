QuillsEnabled Open Bugs
=======================

This file contains tests for bugs not yet fixed.


Issue #143: Portlets do not show up in empty blogs
--------------------------------------------------

This issue is caused by the way BasePortletRenderer implements ``available``.

We do not use one of Quills' portlet here but make our own, as the problem
is located in BasePortletRenderer.

    >>> from plone.app.portlets.portlets import base
    >>> from quills.app.portlets.base import BasePortletRenderer
    >>> class TestRenderer(BasePortletRenderer, base.Renderer):
    ...     """A simple Renderer"""
    ...     pass

Now create a blog. And see if we can get our portlet renderer. We first try
with an empty blog.

    >>> blogFolder = self.portal.weblog
    >>> from zope.component import getMultiAdapter
    >>> view = getMultiAdapter((blogFolder, blogFolder.REQUEST), name='view')
    >>> renderer = TestRenderer(blogFolder, blogFolder.REQUEST, view, None, None)
    >>> renderer.available
    True

Now with one private entry in it.

    >>> entry = blogFolder.invokeFactory('Document', id='entry', title='A blog entry')
    >>> entry = blogFolder[entry]
    >>> renderer.available
    True

And now with that one published. In all three cases the portlet should show up.

    >>> from Products.CMFCore.utils import getToolByName
    >>> wft = getToolByName(self.getPortal(), 'portal_workflow')
    >>> wft.getInfoFor(entry, 'review_state')
    'private'

    >>> wft.doActionFor(entry, 'publish')
    >>> renderer.available
    True


Issue #144:  Syndication AttributeError: getExcerpt
---------------------------------------------------

Syndication is broken in QuillsEnabled svn trunk (rev. 72157) because
the view (e.g. atom.xml) tries to access getExcerpt which is undefined
for ATDocument.

First we create an entry. We cannot immediately adapt from what we get
from addEntry since it already is an adapter (and we do not really of
what portal type). (There cannot be an adapter from IWeblogEntry to
IFeedEntry because this would make it impossible (or hard at least) to
use arbitrary content types for blog contents.)

    >>> entry = self.weblog.addEntry("A blog entry",
    ...              "This is no excerpt.", "Contents here")
    >>> from quills.core.interfaces import IWeblogEntry
    >>> IWeblogEntry.isImplementedBy(entry) 
    True

So we will navigate to the actual content (instead of for instance
calling context on the entry).

    >>> entry = entry.context
    >>> from Products.basesyndication.interfaces import IFeedEntry
    >>> feedAdapter = IFeedEntry(entry)

Now let's see if we can get the correct description.

    >>> feedAdapter.getDescription()
    'This is no excerpt.'

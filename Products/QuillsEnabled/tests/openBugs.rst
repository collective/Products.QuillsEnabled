QuillsEnabled Open Bugs
=======================

This file contains tests for bugs not yet fixed.


Issue #144:  Syndication AttributeError: getExcerpt
---------------------------------------------------

Syndication is broken in QuillsEnabled svn trunk (rev. 72157) because
the view (e.g. atom.xml) tries to access getExcerpt which is undefined
for ATDocument.

First we create an entry.

    >>> entry = self.weblog.addEntry("A blog entry",
    ...              "This is a excerpt.", "Contents here")
    >>> from quills.core.interfaces import IWeblogEntry
    >>> IWeblogEntry.isImplementedBy(entry) 
    True

Now we make it a FeedEntry and try to get it's description.

    >>> from Products.basesyndication.interfaces import IFeedEntry
    >>> feedAdapter = IFeedEntry(entry)
    >>> feedAdapter.getDescription()
    'This is a excerpt.'

The same for the portal type instance wrapped.

    >>> entry = entry.context
    >>> feedAdapter = IFeedEntry(entry)
    >>> feedAdapter.getDescription()
    'This is a excerpt.'


""" This is patch (sic!) in response to Quills issue #172: WeblogEntryView
cannot not be fetched by appending 'view' to the entries location. In essence,
it will hard code the WeblogEntryView for all IPossibleWeblogEntry content
inside a Weblog whose URL is either suffixed with 'view' or has no suffix.

This mechanizm *needs* rework! We are working against Zope/Plone here!
We need to find a way to non-intrusively extend/modify the DynamicType behavior
of a bloggified content type (page, new item, etc).
"""

from quills.core.interfaces import IPossibleWeblogEntry
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides, Interface
import quills.app.traversal

class IInsideWeblog(Interface):
    """Marker interface for Requests to signal that traversal moves
    inside a QuillsEnabled weblog."""

def defaultView(request, obj):
    """Fetch the default WeblogEntryView from the given object, if
    possible. Otherwise return the object itself.
    """
    stack = request['TraversalRequestNameStack']
    if ( (stack == [] or stack == ['view']) and 
        IPossibleWeblogEntry.providedBy(obj)):
        view = queryMultiAdapter((obj, request),
                                 name='weblogentry_view')
        if view is not None:
            request['TraversalRequestNameStack'] = []
            return view.__of__(obj)
    else:
        return obj
    
class WeblogTraverser(quills.app.traversal.WeblogTraverser):
    """Augment the default WeblogTraverse to hard-code a default view
    for WeblogEntries."""
   
    def publishTraverse(self, request, name):
        resolved = super(WeblogTraverser, self).publishTraverse(request, name)
        alsoProvides(request, IInsideWeblog)
        return defaultView(request, resolved)


class WeblogArchiveTraverser(quills.app.traversal.WeblogArchiveTraverser):
    """Augment the default WeblogTraverse to hard-code a default view
    for WeblogEntries."""

    def publishTraverse(self, request, name):
        resolved = super(WeblogArchiveTraverser, self).publishTraverse(request,
                                                                       name)
        return defaultView(request, resolved)



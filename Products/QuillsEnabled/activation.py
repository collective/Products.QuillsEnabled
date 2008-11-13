# zope imports
from zope.interface import implements
from zope.annotation.interfaces import IAnnotations
from zope.lifecycleevent.interfaces import IObjectEvent
from zope.lifecycleevent import ObjectEvent
from Acquisition import aq_base
from BTrees.OOBTree import OOBTree

# plone imports
from plone.portlets.constants import CONTEXT_ASSIGNMENT_KEY, CONTEXT_CATEGORY
from plone.app.portlets.storage import PortletAssignmentMapping

# Quills imports
from quills.app.activation import DEFAULT_LEFT_PORTLETS, DEFAULT_RIGHT_PORTLETS


class IWeblogActivationEvent(IObjectEvent):
    """An event fired when an object is activated as a weblog.
    """

class WeblogActivationEvent(ObjectEvent):
    """
    """
    implements(IWeblogActivationEvent)


class IWeblogDeactivationEvent(IObjectEvent):
    """ An event fired when an weblog is deactivated """


class WeblogDeactivationEvent(ObjectEvent):
    implements(IWeblogDeactivationEvent)



def updateIndexes(obj, event):
    """An event listener that reindexes an object, as well as all of its
    contents (and subcontents, etc) to ensure that content that existed before
    QuillsEnabled was installed is correctly cataloged with the appropriate
    marker interfaces.
    """
    recursivelyCatalog(obj)


def recursivelyCatalog(obj):
    obj.reindexObject()
    obj_base = aq_base(obj)
    if hasattr(obj_base, 'listFolderContents'):
        for each in obj.listFolderContents():
            recursivelyCatalog(each)



def unregisterContextPortlets(obj, event):
    """ An event listener to unregister portltets when blog deactivation
    """

    annotated = IAnnotations(obj)
    portlets = annotated.get(CONTEXT_ASSIGNMENT_KEY, OOBTree())

    left_portlets = portlets.get('plone.leftcolumn', PortletAssignmentMapping())
    right_portlets = portlets.get('plone.rightcolumn', PortletAssignmentMapping())

    for name, assignment, kwargs in DEFAULT_LEFT_PORTLETS:
        if left_portlets.has_key(name):
            del left_portlets[name]
    for name, assignment, kwargs in DEFAULT_RIGHT_PORTLETS:
        if right_portlets.has_key(name):
            del right_portlets[name]

    portlets['plone.leftcolumn'] = left_portlets
    portlets['plone.rightcolumn'] = right_portlets
    annotated[CONTEXT_ASSIGNMENT_KEY] = portlets

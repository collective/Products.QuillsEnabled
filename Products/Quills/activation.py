# zope imports
from zope.interface import implements
from zope.lifecycleevent.interfaces import IObjectEvent
from zope.lifecycleevent import ObjectEvent
from Acquisition import aq_base

class IWeblogActivationEvent(IObjectEvent):
    """An event fired when an object is activated as a weblog.
    """


class WeblogActivationEvent(ObjectEvent):
    """
    """
    implements(IWeblogActivationEvent)


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

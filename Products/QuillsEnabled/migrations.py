"""
Upgrade QuillsEnabled portlets to 1.7
"""
from zope.component import getUtility
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName

from plone.portlets.interfaces import IPortletManager

from quills.core.interfaces import IWeblogEnhanced
from quills.app.portlets.context import INTERFACE_CATEGORY


def removePortletAssignments(setuptool):
    """ Remove portlets assignments done by quills.app setuphandlers in all Quills instances """
    portal = getUtility(ISiteRoot)
    catalog = getToolByName(portal, 'portal_catalog')
    left_column = getUtility(IPortletManager, name='plone.leftcolumn')
    right_column = getUtility(IPortletManager, name='plone.rightcolumn')

    if left_column.get(INTERFACE_CATEGORY, None) is not None:
        del left_column[INTERFACE_CATEGORY]

    if right_column.get(INTERFACE_CATEGORY, None) is not None: 
        del right_column[INTERFACE_CATEGORY]
        
    

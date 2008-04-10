"""Base class for integration tests, based on ZopeTestCase and PloneTestCase.
Note that importing this module has various side-effects: it registers a set of
products with Zope, and it sets up a sandbox Plone site with the appropriate
products installed.
"""

# Zope imports
from zope.interface import alsoProvides

from Testing import ZopeTestCase

# Let Zope know about QuillsEnabled
ZopeTestCase.installProduct('QuillsEnabled')

# Import PloneTestCase - this registers more products with Zope as a side effect
from Products.PloneTestCase.PloneTestCase import PloneTestCase
from Products.PloneTestCase.PloneTestCase import FunctionalTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite

from quills.core.interfaces import IWeblog, IWeblogEnhanced
from quills.app.tests.base import BrowserMixin

# Set up a Plone site, and apply the Quills extension profile
setupPloneSite(products=['QuillsEnabled'])


class QuillsTestCaseMixin(BrowserMixin):
    """Base class for integration tests for the 'Quills' product. This may
    provide specific set-up and tear-down operations, or provide convenience
    methods.
    """

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.portal.invokeFactory('Folder', id='weblog')
        folder = self.portal.weblog
        self.portal.portal_workflow.doActionFor(folder, 'publish')
        alsoProvides(folder, IWeblogEnhanced)
        self.weblog = IWeblog(folder)
        self.weblog_content = folder


class QuillsTestCase(QuillsTestCaseMixin, PloneTestCase):
    """Base class for integration tests for the 'Quills' product. This may
    provide specific set-up and tear-down operations, or provide convenience
    methods.
    """


class QuillsFunctionalTestCase(QuillsTestCaseMixin, FunctionalTestCase):
    """ a class for running functional tests."""


class QuillsDocTestCase(QuillsTestCaseMixin, PloneTestCase):
    """Base class for integration tests for the 'Quills' product. This may
    provide specific set-up and tear-down operations, or provide convenience
    methods.
    """


class QuillsContributorDocTestCase(QuillsDocTestCase):
    """As QuillsDocTestCase, but only gives the logged-in user the 'Contributor'
    role.
    """

    def afterSetUp(self):
        self.setRoles(('Contributor', 'Reviewer'))
        self.portal.invokeFactory('Folder', id='weblog')
        folder = self.portal.weblog
        alsoProvides(folder, IWeblogEnhanced)
        self.weblog = IWeblog(folder)
        self.weblog_content = folder

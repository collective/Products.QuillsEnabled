""" Test remote blogging."""

from Products.CMFCore.utils import getToolByName
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import PloneSite
from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite
from base import QuillsFunctionalTestCase
from quills.remoteblogging.interfaces import IUIDManager
import doctest
import unittest
import zope.component.testing


# Set up a Plone site, most stuff is already done by module 'base'
PloneTestCase.installProduct('MetaWeblogPASPlugin')
PloneTestCase.setupPloneSite(products=['MetaWeblogPASPlugin'])

class TestRemoteBlogging(QuillsFunctionalTestCase):
    """ Integration test for quills.remoteblogging."""

    def afterSetUp(self):
        super(TestRemoteBlogging, self).afterSetUp()
        self.mwenabled = self.weblog_content
        self.appkey = IUIDManager(self.mwenabled).getUID()
        self.blogid = self.appkey
        mtool = getToolByName(self.portal, 'portal_membership')
        self.bloguserid = mtool.getAuthenticatedMember().getId()


def test_suite():
    suite = unittest.TestSuite(())

    dt = ZopeDocFileSuite(
        'metaweblogapi.txt',
        package='quills.remoteblogging.tests',
        test_class=TestRemoteBlogging,
        optionflags=doctest.ELLIPSIS,
        )
    dt.layer = PloneSite
    suite.addTest(dt)

    suite.addTest(doctest.DocTestSuite('quills.app.remoteblogging.uidmanager',
                 setUp=zope.component.testing.setUp,
                 tearDown=zope.component.testing.tearDown))

    suite.addTest(doctest.DocTestSuite('quills.app.remoteblogging.usermanager',
                 setUp=zope.component.testing.setUp,
                 tearDown=zope.component.testing.tearDown))

    return suite

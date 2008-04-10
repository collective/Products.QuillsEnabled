import unittest
from doctest import ELLIPSIS, NORMALIZE_WHITESPACE

from zope.testing import doctest
from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite
from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import PloneSite

from Products.QuillsEnabled.config import PROJECTNAME
from base import QuillsDocTestCase
from base import QuillsContributorDocTestCase
from base import QuillsFunctionalTestCase

# Standard options for DocTests
optionflags = (ELLIPSIS |
    NORMALIZE_WHITESPACE )

ZOPE_DEPS = []
PLONE_DEPS = [PROJECTNAME,]

for x in ZOPE_DEPS + PLONE_DEPS:
    ZopeTestCase.installProduct(x)

PloneTestCase.setupPloneSite(products=PLONE_DEPS)

def test_suite():
    suite = unittest.TestSuite(())


    suite.addTest(ZopeDocFileSuite(
        'workflowstates.txt',
        package='quills.app.tests',
        test_class=QuillsDocTestCase,
        optionflags=optionflags,
        )
    )

    suite.addTest(ZopeDocFileSuite(
        'tests.txt',
        package='quills.core.tests',
        test_class=QuillsDocTestCase,
        optionflags=optionflags,
        )
    )

    suite.addTest(ZopeDocFileSuite(
        'tests.txt',
        package='quills.core.tests',
        test_class=QuillsContributorDocTestCase,
        optionflags=optionflags,
        )
    )

    suite.addTest(ZopeDocFileSuite(
        'tests.txt',
        package='quills.core.tests',
        test_class=QuillsDocTestCase,
        optionflags=optionflags,
        )
    )

    suite.addTest(ZopeDocFileSuite(
        'browser.rst',
        package='Products.QuillsEnabled.tests',
        test_class=QuillsFunctionalTestCase,
        optionflags=optionflags,
        )
    )

    suite.addTest(ZopeDocFileSuite(
        'browser.rst',
        package='quills.app.tests',
        test_class=QuillsFunctionalTestCase,
        optionflags=optionflags,
        )
    )

    suite.addTest(ZopeDocFileSuite(
        'fixedBugs.rst',
        package='quills.app.tests',
        test_class=QuillsFunctionalTestCase,
        optionflags=optionflags,
        )
    )

    suite.addTest(ZopeDocFileSuite(
        'tests.txt',
        package='quills.core.tests',
        test_class=QuillsContributorDocTestCase,
        optionflags=optionflags,
        )
    )

    suite.layer = PloneSite
    return suite

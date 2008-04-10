# Standard library imports
import unittest
from doctest import DocFileSuite, DocTestSuite

# Zope imports
import zope.component.testing

# Quills imports
from quills.core.tests.test_doctests import suites as quills_core_suites
from quills.app.tests.test_doctests import suites as quills_app_suites

def setUp(test):
    pass

suites = (
    DocTestSuite('Products.QuillsEnabled.adapters.document',
                 setUp=zope.component.testing.setUp,
                 tearDown=zope.component.testing.tearDown),
    DocTestSuite('Products.QuillsEnabled.adapters.folder',
                 setUp=zope.component.testing.setUp,
                 tearDown=zope.component.testing.tearDown),
    )

def test_suite():
    return unittest.TestSuite(suites + quills_core_suites + quills_app_suites)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
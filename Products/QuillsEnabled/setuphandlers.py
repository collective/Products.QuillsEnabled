# Standard library imports
from StringIO import StringIO

# Zope imports
from transaction import commit

# Plone imports
from Products.CMFCore.utils import getToolByName

# Quills imports
from quills.app.setuphandlers import setup_gs_profiles
from quills.app.setuphandlers import weblogPortletSetup

# Local imports
import config


def importFinalSteps(context):
    """Install Quills."""
    # Only run step if a flag file is present
    # see http://maurits.vanrees.org/weblog/archive/2007/06/discovering-genericsetup
    if context.readDataFile('quillsenabled_product_various.txt') is None:
        return
    out = StringIO()
    # install dependencies
    portal = context.getSite()
    quickinstaller = portal.portal_quickinstaller

    for dependency in config.DEPENDENCIES:
        print >> out, u"Installing dependency %s:" % dependency
        quickinstaller.installProduct(dependency)
        commit()

    setup_gs_profiles(portal, config.GS_DEPENDENCIES, out)
    weblogPortletSetup(portal, out)
    print >> out, u"Successfully installed %s." % config.PROJECTNAME
    return out.getvalue()


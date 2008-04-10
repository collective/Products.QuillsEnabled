# Standard library imports
from StringIO import StringIO

# Zope imports
import transaction

# CMF imports
from Products.CMFCore.utils import getToolByName

# Plone imports
from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin

# Local imports
from Products.QuillsEnabled import config

EXTENSION_PROFILES = ('Products.QuillsEnabled:default',)

def install(self):
    """Install QuillsEnabled.
    """
    out = StringIO()

    portal = getToolByName(self,'portal_url').getPortalObject()
    portal_setup = getToolByName(self, 'portal_setup')
    quickinstaller = portal.portal_quickinstaller
    for dependency in config.DEPENDENCIES:
        print >> out, u"Installing dependency %s:" % dependency
        quickinstaller.installProduct(dependency)
        transaction.savepoint()
    # Register CSS
    #registerStylesheets(self, out)

    for extension_id in EXTENSION_PROFILES:
        portal_setup.runAllImportStepsFromProfile('profile-%s' % extension_id, purge_old=False)
        transaction.savepoint()

    install_subskin(self, out, config.GLOBALS)

    # Keep some of our types out of the navtree
    #updateNavtreeProperties(self, out)
    # Allow Weblogs to be used as the front page of a site
    # FIXME: When this is enabled there is no way to add an Entry to the blog
    #updateDefaultPageTypes(self)
    #permissions.setupPortalSecurity(self, out)
    #automigrate(self, out)
    #updateSchemas(self, out)

    print >> out, u"Successfully installed %s." % config.PROJECTNAME
    return out.getvalue()


def registerStylesheets(self, out):
    """Register CSS with the registry.
    """
    csstool = getToolByName(self, 'portal_css')
    existing = csstool.getResourceIds()
    updates = []
    for css in config.STYLESHEETS:
        if not css.get('id') in existing:
            csstool.registerStylesheet(**css)
            print >> out, u"Registered stylesheet %s." % css.get('id')
        else:
            updates.append(css)
    if updates:
        _updateResources(csstool, updates)


def unregisterStylesheets(self):
    """Remove Quills CSS from the registry.
    """
    registry = getToolByName(self, 'portal_css')
    registry.unregisterResource('Quills.css')


def uninstall(self):
    """Uninstall QuillsEnabled.
    """
    out = StringIO()
    portal_controlpanel = getToolByName(self, 'portal_controlpanel')
    portal_controlpanel.unregisterApplication(config.PROJECTNAME)
    unregisterStylesheets(self)
    #permissions.unsetupPortalSecurity(self, out)
    print >> out, u"Successfully uninstalled %s." % config.PROJECTNAME
    return out.getvalue()


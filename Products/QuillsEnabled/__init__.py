# Plone imports
from Products.CMFCore.DirectoryView import registerDirectory

# Local imports
import config

registerDirectory(config.SKINS_DIR, config.GLOBALS)
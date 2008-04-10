About
=====

QuillsEnabled is a Weblog System for the Plone content management system.  Based on
the Quills codebase, it is a rewrite that seeks to make it possible to apply
weblog look, feel, and functionality to standard Plone objects.  Currently, that means
it is possible to mark a 'Folder' object as a weblog, and then have that folder displayed
accordingly, with all of its contained 'Page' objects treated as weblog entries.

WARNING: This is currently only alpha quality code!  It is under-tested, and some of the UI
         is incomplete.  Most notably, I have yet to wire things up so that you can mark
         folders as weblogs from the Plone 'display' menu (as with Plone4ArtistsCalendar).
         In order to enable the weblog features for a folder, you currently need to use the
         ZMI to declare that your folder also provides the 'quills.core.interfaces.IWeblogEnhanced'
         interface.  That should be enough to test the basic functionality, although the
         weblog configuration view will still not be linked to in the actions.  You should
         visit [path/to/your/folder]/config_view to change settings.


Dependencies
============

Requires
--------

  o Zope 2.10.4+

  o Plone 3

  o In you Products directory:

    o basesyndication

    o fatsyndication

  o In you lib/python/ (see note below)

    o quills.core

    o quills.app


Acknowledgements
================

Google's 'Summer of Code' supported me (Tim Hicks) for several months in 2007
to further develop the Quills product - for which I'm very grateful.


Resources
=========

    Development Homepage:  http://plone.org/products/quills/
    Bug Tracker:           http://plone.org/products/quills/issues/
    Mailing List:          http://lists.etria.com/cgi-bin/mailman/listinfo/quills-dev
    Subversion Repository: https://svn.plone.org/svn/collective/QuillsEnabled/


Other Zope/Plone Weblog Products
================================

Plone Compatible:
    CMFWeblog   http://www.sf.net/projects/collective/
    SimpleBlog  http://www.sf.net/projects/collective/
    COREBlog    http://coreblog.org/
    EasyBlog    http://plone.org/products/easyblog/


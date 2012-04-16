======================
Products.QuillsEnabled
======================

Quills is an Enterprise Weblog System for the Plone content management system.
It is designed from the ground up to work well and provide specialized features
for a multi-blog, multi-user environment.

Requires Plone 3.1 or later.

Getting started
===============

Products.QuillsEnabled is a newer more lightweight and future-proof replacement
for Products.Quills.

It improves upon Products.Quills by not implementing it's own portal types but
instead gives you blogging capabilities with Plone's internal content types 
by marking them with special interfaces.

QuillsEnabled allows you to use Plone Folders, Documents and News Items for
blogging. To create a blog, simply add a new Folder and select
"Activate Blog" from the "Actions" menu, then add Pages/New Items for each
new post. Existing folders can be turned into a blog the same way. To change
a Blog back into a plain and boring folder, select "Deactive blog"
from the Actions menu.


Extensions
==========

There are a few packages that add extra functionality to your Blog.

quills.remoteblogging
    Use your Blog with any Weblog Editor that supports the `MetaWeblog API`_.
    This feature requires the ``Products.MetaWeblogPASPlugin`` product to
    be installed into your Plone site.

    .. _MetaWeblog API: http://www.metaweblogapi.com/


Links
=====

Product Homepage
    Visit `http://plone.org/products/quills`__ to learn more about Quills.

    __ http://plone.org/products/quills

Mailing List
    Read our mailing list archive at `Google Groups`__, or subscribe to it
    there. To post, write an e-mail to `plone-quills@googlegroups.com`__.
    
    __ http://groups.google.com/group/plone-quills
    __ plone-quills@googlegroups.com

Issue Tracker
    Report bugs and request features by using the `issue tracker`__ on our
    product homepage.

    __ http://plone.org/products/quills/issues


Code Repository
    You can find the source code in the Plone Collective Repository at
    `https://github.com/collective/Products.QuillsEnabled/`__.

    __ https://github.com/collective/Products.QuillsEnabled


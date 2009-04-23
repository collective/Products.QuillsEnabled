QuillsEnabled fixed Bugs
========================

Issue #179: Quills breadcrumbs break the Static Text Portlet globally
---------------------------------------------------------------------

To test for this issue we will simply add a static text portlet to a
page. This page need not be inside a Blog!

    >>> id = self.portal.invokeFactory("Document", id="issue179",
    ...           title="Issue 179", description="A test case for issue #179.")

Now assign the Static Text Portlet. The issue happens only through the web,
and gives quite some stack trace.

    >>> self.setRoles(("Manager",))
    >>> browser = self.getBrowser(logged_in=True)
    >>> browser.handleErrors = False
    >>> browser.open("http://nohost/plone/%s/@@manage-portlets" % (id,))
    >>> selectBox = browser.getControl(name=":action", index=0)
    >>> selectBox.getControl(label="Static text portlet").selected = True
    >>> # selectBox.displayValue=["Static text portlet"]
    >>> browser.getControl(label="Add portlet", index=1).click()
    >>> "Add static text portlet" in browser.contents
    True

The same might happen inside a blog, of course.

    >>> url = self.weblog.addEntry("Issue 179", "This is a excerpt.",
    ...                              "Contents here", id="issue179").getId()
    >>> browser.open("http://nohost/plone/weblog/%s/@@manage-portlets" % (id,))
    >>> selectBox = browser.getControl(name=":action", index=0)
    >>> selectBox.getControl(label="Static text portlet").selected = True
    >>> # selectBox.displayValue=["Static text portlet"]
    >>> browser.getControl(label="Add portlet", index=1).click()
    >>> "Add static text portlet" in browser.contents
    True

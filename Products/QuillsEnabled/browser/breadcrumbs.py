from zope.interface import implements
from zope.component import getMultiAdapter
from Acquisition import aq_base

from Products.Five import BrowserView

from Products.CMFPlone.browser.interfaces import INavigationBreadcrumbs
from Products.CMFPlone.browser.navigation import PhysicalNavigationBreadcrumbs

from quills.core.interfaces import IWeblogEntry


class ArchiveAwareBreadcrumbs(BrowserView):

    implements(INavigationBreadcrumbs)

    def breadcrumbs(self):
        """This method should return a tuple of the form:

            ({'absolute_url': url_value,
                     'Title': title_value,
             },)
        """
        context = self.context
        # This is *horrible*.  It seems like Five munges this view class to
        # subclass Acquisition.Explicit, which then gives us an acquisition
        # chain looking like self.context -> self (and that's it). What we want
        # is the proper aq_chain back up through the weblog archive hierarchy
        # that we have traversed through. That correct chain is available from
        # the request...
        request = self.request
        # However, sometimes context can be what we expect to be parent because
        # we have a view as the last path segment. So...
        if aq_base(request['PARENTS'][0]) == aq_base(context):
            container = request['PARENTS'][1]
        else:
            container = request['PARENTS'][0]
        view = getMultiAdapter((container, request), name='breadcrumbs_view')
        crumbs = tuple(view.breadcrumbs())
        crumbs += ({'absolute_url': context.absolute_url(),
                   'Title': IWeblogEntry(context).getTitle(),
                   },)
        return crumbs

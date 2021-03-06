# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.component import getMultiAdapter

from Acquisition import aq_inner
from Products.Five import BrowserView

from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.LinguaPlone.browser.selector import TranslatableLanguageSelector
from plonetheme.urbanisme.browser.interfaces import IThemeView
from plone.app.layout.viewlets.common import SearchBoxViewlet as SearchBoxBase
import os

_marker = []

class LogoViewlet(ViewletBase):
    render = ViewPageTemplateFile('templates/logo.pt')
    
    def languages(self):
        """Returns list of languages."""
        if self.tool is None:
            return []
        bound = self.tool.getLanguageBindings()
        current = bound[0]
        
    def logo(self):
        lang = self.context.Language()
        if lang == "nl":
            src="%s/logo-nl.jpg" % self.site_url
            alt="Ruimtelijke ordening & Stedenbouw in het Brussels Hoofdstdelijk Gewest"
        else:
            src="%s/logo.jpg"  % self.site_url
            alt="Aménagement du teritoire & L'urbanisme en Région Bruxelles-Capitale"
        if os.environ.get("DEPLOY_ENV") == "staging":
            src="%s/logo_staging_%s.jpg" % (self.site_url, lang)
        return {"src":src, "alt":alt}

class LanguageSelector(TranslatableLanguageSelector):
    render = ViewPageTemplateFile('templates/languageselector.pt')

class Quicklinks(ViewletBase):
    render = ViewPageTemplateFile('templates/quicklinks.pt')

class SearchBoxViewlet(SearchBoxBase):
    render = ViewPageTemplateFile('templates/searchbox.pt')


class ThemeView(BrowserView):
    implements(IThemeView)

    # Utility methods

    def getColumnsClass(self, view=None):
        """Determine whether a column should be shown. The left column is called
        plone.leftcolumn; the right column is called plone.rightcolumn.
        """
        context = aq_inner(self.context)
        plone_view = getMultiAdapter((context, self.request), name=u'plone')
        sl = plone_view.have_portlets('plone.leftcolumn', view=view);
        sr = plone_view.have_portlets('plone.rightcolumn', view=view);
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')

        if not sl and not sr:
            # we don't have columns, thus conten takes the whole width
            return "cell width-full position-0"
        elif sl and sr:
            # In case we have both columns, content takes 50% of the whole
            # width and the rest 50% is spread between the columns
            return "cell width-1:2 position-1:4"
        elif (sr and not sl) and (portal_state.is_rtl()):
            # We have right column and we are in RTL language
            return "cell width-3:4 position-1:4"
        elif (sr and not sl) and (not portal_state.is_rtl()):
            # We have right column and we are NOT in RTL language
            return "cell width-3:4 position-0"
        elif (sl and not sr) and (portal_state.is_rtl()):
            # We have left column and we are in RTL language
            return "cell width-3:4 position-0"
        elif (sl and not sr) and (not portal_state.is_rtl()):
            # We have left column and we are in NOT RTL language
            return "cell width-3:4 position-1:4"

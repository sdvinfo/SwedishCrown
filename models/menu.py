# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B(SPAN('S'),'wedish',SPAN('C'),'rown ', SPAN('CMS')),XML('&trade;&nbsp;'),
                  _class="brand",_href=URL('default', 'index'))
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Dmitriy Serezhin <sdvinfo@gmail.com>'
response.meta.description = 'CMS for homeowners association Swedish Crown'
response.meta.keywords = 'ТСЖ, CMS, ЖКХ'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('About CMS'), False, URL('default', 'index'), []),
    (T('HOA information'), False, URL('default','about'), [
        (T('Common information'), False, URL('default','common_info'), []),
        (T('Tariff information'), False, URL('default','tariff_info'), []),
        (T('Management Company'), False, URL('default','management_company_info'), []),
        (T('Documents'), False, URL('default', 'documents'), []),
        (T('Photos'), False, URL('default', 'photos'), []),
    ]),
    # (T('News'), False, URL('default', 'news'), []),
    # (T('FAQ'), False, URL('default', 'faq'), []),
    (T('Forum'), False, URL('default','forum'), []),
    # (T('Links'), False, URL('default', 'links'), []),
    (T('Personal page'), False, URL('profile','personal_page')),

]

# if auth.is_logged_in():
#     response.menu += [
#         (T('Personal page'), False, URL('profile','personal_page')),
#     ]



# if "auth" in locals(): auth.wikimenu()

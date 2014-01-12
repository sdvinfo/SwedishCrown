# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    #response.flash = T("Welcome to web2py!")
    response.title = 'Добро пожаловать в Swedish Crown CMS!'
    #response.left_sidebar_enabled = True
    response.right_sidebar_enabled = True

    return dict(message='')
    #return auth.wiki()
    #return locals()


def about():
    redirect('common_info')
    return locals()


def common_info():
    response.title = 'ТСЖ "Шведская Крона"'
    return locals()


def tariff_info():
    return locals()


def management_company_info():
    return locals()


def documents():
    return locals()


def photos():
    return locals()


def news():
    return locals()


def faq():
    return locals()


def forum():
    redirect('http://www.swedkrona.ru')
    return locals()


def links():
    return locals()














# <tr id="auth_user_first_name__row">
# <tr id="auth_user_last_name__row">
# <tr id="auth_user_email__row">
# <tr id="auth_user_password__row">
# <tr id="auth_user_password_two__row">
# <td class="w2p_fl">
# <label>Повторите пароль: </label>
# </td>
# <td class="w2p_fw">
# <input class="password" type="password" name="password_two">
# </td>
# <td class="w2p_fc">please input your password again</td>
# </tr>
# <tr id="auth_user_middle_name__row">
# <tr id="auth_user_apartment__row">
# <tr id="auth_user_house__row">
# <tr id="auth_user_personal_info__row">
# <tr id="submit_record__row">



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    if request.args(0)=='profile':
        redirect(URL('profile','index'))
    # elif request.args(0)=='register':
    #     return dict(form=auth(_next='/SwedishCrown/default/user/profile'))
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())


# This code added support for autocompletion in most of IDE
if False:
    from gluon import *
    from db import *  #repeat for all models
    from menu import *

    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T

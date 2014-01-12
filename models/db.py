# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()
if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()



# Добавим свои поля в таблицу auth_user
# auth.settings.extra_fields['auth_user'] = [
#      Field('middle_name','string',label=T('Middle name')),
#      Field('house','reference house',label=T('House'),requires = IS_IN_DB(db,'house.id','%(building)s',zero=T('Choose your house'))),
#      Field('flat','reference flat',label=T('Apartment')),
#      Field('personal_info','text',label=T('Personal information')),
#      Field('role_id', 'integer', notnull=True, default=3, requires = IS_IN_SET([(2, 'admin'), (3, 'resident'), (4, 'guest')]))  # (`role_id` int(11) NOT NULL DEFAULT '0',)
#     ]
# db.auth_user.house.requires = IS_IN_DB(db.house.id,'%(building)s')



## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'sdvinfo@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False  # Подтверждение регистрации по почте
auth.settings.reset_password_requires_verification = True
# auth.settings.login_after_registration = True # Автоматические вход в систему после регистрации
# auth.settings.create_user_groups = False


# def onaccept(form): # form accepted
#     auth.add_membership(form.vars.role_id, form.vars.id)
#
# auth.settings.register_onaccept.append(onaccept)
#



#db.define_table('flat',
#                Field('num', db.auth_user,
#                      requires = IS_IN_DB(db,'auth_user.id','%s(flat_number)s'),
#                      represent=lambda id, n: db.auth_user(id).flat_number))






## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

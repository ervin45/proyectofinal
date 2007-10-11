from turbogears import controllers, expose, flash
# from model import *
from turbogears import identity, redirect
from cherrypy import request, response



import string

from model import xmlaResponse

# from bielerDW import json
# import logging
# log = logging.getLogger("bielerDW.controllers")

class Root(controllers.RootController):
    mdx = "hola soy el MDX"
    
    @expose(template="bielerDW.templates.index")
    # @identity.require(identity.in_group("admin"))
    def index(self):
        import time
        # log.debug("Happy TurboGears Controller Responding For Duty")
        flash("Your sdfsdf is now running")
        return dict(now=time.ctime())
    
    @expose(template="bielerDW.templates.content_default")
    def content_default(self):
        # log.debug("Happy TurboGears Controller Responding For Duty")
        return dict(title="HOLA")
    
    @expose(template="bielerDW.templates.reportes")
    def reportes(self, title):
        xmla = xmlaResponse()
        
        if(title == "1"):
            table = xmla.response1("select Crossjoin({[Measures].[Unit Sales]},[Product].[All Products].[Drink].[Alcoholic Beverages].[Beer and Wine].[Beer].Children) ON COLUMNS,  {[Time].[1997]} ON ROWS from [Sales]")
        elif(title == "2"):
            table = xmla.response2("select Crossjoin({[Measures].[Unit Sales]},[Product].[All Products].[Drink].[Alcoholic Beverages].[Beer and Wine].[Beer].Children) ON COLUMNS,  {[Time].[1997]} ON ROWS from [Sales]")            
        else:            
            table = xmla.response3("select Crossjoin({[Measures].[Unit Sales]},[Product].[All Products].[Drink].[Alcoholic Beverages].[Beer and Wine].[Beer].Children) ON COLUMNS,  {[Time].[1997]} ON ROWS from [Sales]")            
            
	# log.debug("Happy TurboGears Controller Responding For Duty")
	title = title[0].upper() + title[1:]
        return dict(title=title, filas=table, pt=self.mdx, link=(int(title) + 1))
    

    @expose(template="bielerDW.templates.login")
    def login(self, forward_url=None, previous_url=None, *args, **kw):

        if not identity.current.anonymous \
            and identity.was_login_attempted() \
            and not identity.get_identity_errors():
            raise redirect(forward_url)

        forward_url=None
        previous_url= request.path

        if identity.was_login_attempted():
            msg=_("The credentials you supplied were not correct or "
                   "did not grant access to this resource.")
        elif identity.get_identity_errors():
            msg=_("You must provide your credentials before accessing "
                   "this resource.")
        else:
            msg=_("Please log in.")
            forward_url= request.headers.get("Referer", "/")
            
        response.status=403
        return dict(message=msg, previous_url=previous_url, logging_in=True,
                    original_parameters=request.params,
                    forward_url=forward_url)

    @expose()
    def logout(self):
        identity.current.logout()
        raise redirect("/")

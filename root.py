import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
from api import API
lookup = TemplateLookup(directories=['html'])
class Root(object):
    api = API()
    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect('/balance')

    @cherrypy.expose
    def balance(self):
        tmpl = lookup.get_template("balance.html")
        out = tmpl.render()
        return out

    @cherrypy.expose
    def info(self):
        tmpl = lookup.get_template("info.html")
        out = tmpl.render()
        return out

    @cherrypy.expose
    def send(self):
        tmpl = lookup.get_template("send.html")
        out = tmpl.render()
        return out

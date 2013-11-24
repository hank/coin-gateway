import cherrypy
import json
def make_error(msg):
    cherrypy.response.status = 500
    return json.dumps({"error": msg})

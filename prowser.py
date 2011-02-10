from bottle import route, run
from bottle import debug as bottle_debug
import settings
import os

bottle_debug = settings.DEBUG


@route('/:requested_path#.+#')
def index(requested_path):
    """ The whole enchilada. 

    Since we will be doing a lot of processing on the path string, accept the
    entire path in one view and pull out the pieces we need from it below. 
    """

    path, filename = os.path.split(requested_path)

    if filename:
        return "Trying to access file"

    else:
        return "Trying to access folder"



if settings.DEBUG:
    run(host="localhost", port=8080, reloader=settings.DEBUG)

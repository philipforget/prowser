import os, errno, sys
import bottle
from bottle import route, run, static_file, error
from bottle import jinja2_view as view
from bottle import debug as bottle_debug
from functools import partial
import Image
import urllib

import settings

bottle_debug(settings.DEBUG)

def return_image(path, file, width=None, height=None):
    file_to_return = os.path.join(path, file)
    if not os.path.isfile(os.path.join(settings.DOCUMENT_ROOT, file_to_return)):
        return error404("File not found: %s" % file_to_return)

    # If we are going to be resizing, create the resize directory
    if width or height:
        resize_directory = os.path.join(path, '.resized')
        mkdir_p(os.path.join(settings.DOCUMENT_ROOT, resize_directory))
        # At most you may end up with 2 images of the same size with different filenames but this will speed up caching
        filename = "%sx%s-%s" % (str(width) if width else "*", str(height) if height else "*", file)

        # If the file already exists, return it
        if os.path.isfile(os.path.join(settings.DOCUMENT_ROOT, resize_directory, filename)):
            return static_file(os.path.join(resize_directory, filename), root=settings.DOCUMENT_ROOT)

        try:
            image = Image.open(os.path.join(settings.DOCUMENT_ROOT, file_to_return))
            original_width, original_height = image.size

            if width > original_width or height > original_height:
                return static_file(os.path.join(path, file), root=settings.DOCUMENT_ROOT)

            if width and height:
                image.thumbnail((width, height), Image.ANTIALIAS)

            elif width:
                new_height = (width * original_height) / original_width
                image.thumbnail((width, new_height), Image.ANTIALIAS)

            elif height:
                new_width = (height * original_width) / original_height
                image.thumbnail((new_width, height), Image.ANTIALIAS)

            image.save(os.path.join(settings.DOCUMENT_ROOT, resize_directory, filename))
            return static_file(os.path.join(resize_directory, filename), root=settings.DOCUMENT_ROOT)

        except IOError as e:
            return error404("Could not create file %s" % e)

    return static_file(os.path.join(path, file), root=settings.DOCUMENT_ROOT)


@view('templates/list_dir')
def return_directory(path):
    directory = os.path.abspath(os.path.join(settings.DOCUMENT_ROOT, path))
    # Make sure people arent trying to travese directories
    if directory.find(settings.DOCUMENT_ROOT) == -1:
        return error404("y u try traversing directories?")

    images     = []
    folders    = []
    for file in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, file)):
            if file[0] != "." and file[0] != "_":
                folders.append(urllib.quote(file))
        elif len(os.path.splitext(file)) and os.path.splitext(file)[-1].lower() in settings.IMAGE_EXTENSIONS:
            images.append(urllib.quote(file))

    return dict(path=path, images=images, folders=folders)


def mkdir_p(path):
    """ Simple mkdir -p functionality for python """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else: raise


MODIFIERS = {
    "_thumb":  partial(return_image, width=128, height=128),
    "_small":  partial(return_image, width=400, height=400),
    "_medium": partial(return_image, width=1000, height=1000),
    "_large":  partial(return_image, width=2400, height=2400),
}
MODIFIERS_WITH_ARGUMENTS = {
    "_h_": return_image,
    "_w_": return_image,
}

@error(404)
def error404(error):
    return error

# You should really be using nginx for this, but it's ok!
@route('/static/:filename')
def server_static(filename):
    return static_file(filename, root=settings.STATIC_ROOT)

@route('/')
@route('/:requested_path#.+#')
def index(requested_path=None):
    """ The whole enchilada. 

    Since we will be doing a lot of processing on the path string, accept the
    entire path in one view and pull out the pieces we need from it below. 
    """

    if requested_path:
        path, filename = os.path.split(requested_path)
    else:
        path     = ""
        filename = None

    if filename:
        filename = urllib.unquote(filename)
        path_array = path.strip("/").lstrip("./").lstrip("../").split("/")

        if os.path.isdir(os.path.join(settings.DOCUMENT_ROOT, requested_path)):
            return return_directory(requested_path)

        # Modifier without argument
        if len(path_array) and path_array[0] in MODIFIERS.keys():
            return MODIFIERS[path_array[0]]("/".join(path_array[1:]), filename)

        # Modifier with argument
        elif len(path_array) > 1 and path_array[0] in MODIFIERS_WITH_ARGUMENTS.keys():
            func = MODIFIERS_WITH_ARGUMENTS[path_array[0]]
            try:
                arg = int(path_array[1])
                arg = arg if arg > 0 else -1 * arg
                if arg == 0:
                    return error404("Invalid size")
                return func("/".join(path_array[2:]), filename, arg)
            except ValueError:
                return error404("Invalid argument type provided: %s" % path_array[1])

        return return_image(path, filename)
        
    return return_directory(path)

application = bottle.default_app()

from bottle import route, run, static_file, error, template
from bottle import debug as bottle_debug
import settings
import os, errno
import Image

bottle_debug(settings.DEBUG)

# Modifiers: must return a static_file or 404
def thumb(path, file):
    return return_image(path, file, width=128, height=128)

def small(path, file):
    return return_image(path, file, width=400, height=400)

def medium(path, file):
    return return_image(path, file, width=1000, height=1000)

def large(path, file):
    return return_image(path, file, width=2400, height=2400)

def height_relative(path, file, height):
    return return_image(path, file, height=height)

def width_relative(path, file, width):
    return return_image(path, file, width=width)

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
                print new_height
                image.thumbnail((width, new_height), Image.ANTIALIAS)

            elif height:
                new_width = (height * original_width) / original_height
                print new_width
                image.thumbnail((new_width, height), Image.ANTIALIAS)

            image.save(os.path.join(settings.DOCUMENT_ROOT, resize_directory, filename))
            return static_file(os.path.join(resize_directory, filename), root=settings.DOCUMENT_ROOT)

        except IOError as e:
            return error404("Could not create file %s" % e)

    return static_file(os.path.join(path, file), root=settings.DOCUMENT_ROOT)

def return_directory(path):
    # DOES NOT WORK YET!
    return "Listing %s" % path
    images  = []
    folders = []
    for file in os.listdir(os.path.join(settings.DOCUMENT_ROOT, path)):
        if os.path.isdir(os.path.join(settings.DOCUMENT_ROOT, path, file)):
            if file[0] != "." and file[0] != "_":
                folders.append(file)
        elif len(os.path.splitext(file)) and os.path.splitext(file)[-1].lower() in settings.IMAGE_EXTENSIONS:
            images.append(file)

        print os.path.splitext(file)

    print images
    print folders
    return "Listing dir"

def mkdir_p(path):
    """ Simple mkdir -p functionality for python """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else: raise

MODIFIERS = {
    "_thumb":  thumb,
    "_small":  small,
    "_medium": medium,
    "_large":  large,
}
MODIFIERS_WITH_ARGUMENTS = {
    "_w_":     width_relative,
    "_h_":     height_relative,
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
        path_array = path.strip("/").split("/")

        # Modifier without argument
        if len(path_array) and path_array[0] in MODIFIERS.keys():
            return MODIFIERS[path_array[0]]("/".join(path_array[1:]), filename)

        # Modifier with argument
        elif len(path_array) > 1 and path_array[0] in MODIFIERS_WITH_ARGUMENTS.keys():
            func = MODIFIERS_WITH_ARGUMENTS[path_array[-2]]
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



if settings.DEBUG:
    run(host="localhost", port=8080, reloader=settings.DEBUG)

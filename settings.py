import os

DEBUG            = True
STATIC_ROOT      = os.path.expanduser("~/workspace/prowser/static")
DOCUMENT_ROOT    = os.path.expanduser("~/workspace/prowser/documents")
TEMPLATES_DIR    = os.path.join(os.path.dirname(__file__), "templates")
IMAGE_EXTENSIONS = [
    "png",
    "jpg",
    "jpeg",
]

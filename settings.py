import os

DEBUG            = True
PROJECT_DIR      = os.path.dirname(__file__)
STATIC_ROOT      = os.path.join(PROJECT_DIR, "static")
TEMPLATES_DIR    = os.path.join(PROJECT_DIR, "templates")
DOCUMENT_ROOT    = os.path.expanduser("~/Documents")
IMAGE_EXTENSIONS = [
    ".png",
    ".jpg",
    ".jpeg",
]

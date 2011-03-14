import os

DEBUG            = False
PROJECT_DIR      = os.path.dirname(__file__)
STATIC_ROOT      = os.path.join(PROJECT_DIR, "static")
TEMPLATES_DIR    = os.path.join(PROJECT_DIR, "templates")
# DOCUMENT_ROOT Set this in your local_settings.py
#DOCUMENT_ROOT
IMAGE_EXTENSIONS = [
    ".png",
    ".gif",
    ".jpg",
    ".jpeg",
]

from local_settings import *

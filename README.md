A simple image browser with a REST api for requesting resized versions of each image.

Use bootstrap.sh to create a new virtualenv in the project root and install the requirements found in requirements.pip

REST API:

/<folder>
    Lists the contents of the folder
/<folder>/small/<image>
    Returns a small version of the image. What the medium constants means in terms of size can be configured in the root access.txt and overridden in specific folders.
/<folder>/medium/<image>
    Returns a medium version of the image.
/<folder>/large/<image>
    Returns a large version of the image.
/<folder>/w_<int>/<image>
    Returns a version of the image resized proportionately  to width of <int>.
/<folder>/h_<int>/<image>
    Returns a version of the image resized proportionately to height of <int>.

Hitting a folder will list the images and folders contained within it. Each folder can contain an access.txt file which dictates the permissions of the folder and any content within it. 

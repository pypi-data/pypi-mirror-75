==============================
 Mapillary Tools for Python 3
==============================


Tool to upload discrete images to Mapillary.  Does not support videos.


Rewrite
=======

This is a complete rewrite of a portion of the official Mapillary tools found at:
https://github.com/mapillary/mapillary_tools

The official Mapillary tools are broken because Python 2 is dead.  Major
distributions have already removed Python 2 from their standard installation.  A
Python 3 port has been requested a long time ago but nothing happened.

A quick look at the official code shows that it is not worth porting anyway.
That code was obviously written by lots of different people with varying
understanding of Python and then duct-taped together to make it look like one
application.  It also pulls in way too many dependencies, like a full image
manipulation library, 2 different Exif libraries (one of them custom patched)
and an advanced keystore.

The rewritten code uses Python 3 and only a few external libraries.

This code does not change your image files, neither does it copy them.  All data
is put into small sidecar files.  This keeps your disk lean and your backups
small.


Usage
=====

1. Authorize: This will prompt for your Mapillary password:

   .. code-block:: shell

      mapillary_auth.py --user_name <your_username> --user_email <your_email>

   This step is needed only once.  Your credentials are now stored in the file
   :file:`~/.config/mapillary/configs/<CLIENT_ID>`.  Keep this file secret.
   Mapillary credentials do not expire.


2. Pre-process the images:

   .. code-block:: shell

      mapillary_process.py ~/Pictures/Mapillary/*.jpg

   This step extracts GPS data from your images and stores it in sidecar files.


3. Upload the images:

   .. code-block:: shell

      mapillary_upload.py ~/Pictures/Mapillary/*.jpg

   The script remembers which images were successfully uploaded.  If you run the
   upload script on the same images again, the ones already uploaded will not be
   uploaded again.

Run the scripts with '-h' to see more options.


GPS Tracks
==========

This code has no support for GPS tracks.

To use GPS information stored in a GPS track use exiftool to insert GPS
information into your image files, then proces them.

  https://exiftool.org/geotag.html

#!/usr/bin/python3

'''Extract EXIF info from discrete image files.

Extract Latitude, Longitude, Altitude, DateTime and Heading from the image files
and put the information into sidecar files (same filename with an added extension
of .mapillary).

Process images from a directory:

  mapillary_process.py ~/Pictures/Mapillary/*.jpg

Process images from a list of images (one complete filepath per line):

  mapillary_process.py @picture_list.txt
  find ~/Pictures/Mapillary -name "*.jpg" | mapillary_process.py @/dev/stdin

'''

import argparse
import sys
import uuid

from mapillary_tools import get_image_geotags, read_sidecar_file, write_sidecar_file


def build_parser ():
    ''' Build the commandline parser. '''

    parser = argparse.ArgumentParser (
        description = __doc__,
        formatter_class = argparse.RawDescriptionHelpFormatter,  # don't wrap my description
        fromfile_prefix_chars = '@'
    )

    parser.add_argument (
        'images', metavar='FILENAME', type=str, nargs='+',
        help='the images to process'
    )

    parser.add_argument (
        '-v', '--verbose', dest='verbose', action='count',
        help='increase output verbosity', default=0
    )
    return parser


if __name__ == '__main__':
    args = build_parser ().parse_args ()

    for image in args.images:
        geotags = read_sidecar_file (image)
        geotags.setdefault ('MAPPhotoUUID', str (uuid.uuid4 ()))
        geotags.update (get_image_geotags (image))

        if args.verbose:
            print (image, geotags)

        write_sidecar_file (image, geotags)

        if 'MAPLatitude' not in geotags or 'MAPCaptureTime' not in geotags:
            sys.stderr.write ('No GPS data found in {filename}\n'.format (filename = image))

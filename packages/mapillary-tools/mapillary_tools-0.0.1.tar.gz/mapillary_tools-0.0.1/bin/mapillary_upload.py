#!/usr/bin/python3

''' Upload images to Mapillary.

Sorts images into sequences and uploads them to the Mapillary server.

Upload images from a directory:

  mapillary_upload.py ~/Pictures/Mapillary/*.jpg
  mapillary_upload.py -n -v ~/Pictures/Mapillary/*.jpg
  mapillary_upload.py -d 50 -t 5 ~/Pictures/Mapillary/*.jpg

Upload images from a list of images (one complete filepath per line):

  mapillary_upload.py @picture_list.txt
  list_builder | mapillary_upload.py @/dev/stdin

'''

import argparse
import itertools
import json
from multiprocessing.dummy import Pool
import operator
import sys

import requests
from tqdm import tqdm

from mapillary_tools import read_config_file, read_sidecar_file, \
    cut_sequences, managed_session, upload_image

SEQUENCE_THREADS = 2 # upload this many sequences in parallel
UPLOAD_THREADS   = 2 # upload this many images in parallel per sequence

DEFAULT_MAX_TIME = 5 * 60.0 # in seconds. max time between images in same sequence
DEFAULT_MAX_DIST = 100.0    # in meters.  max distance between images in same seq.
DEFAULT_MAX_DOP  = 20.0     # discard images with GPS DOP greater than this

def build_parser ():
    ''' Build the commandline parser. '''

    parser = argparse.ArgumentParser (
        description = __doc__,
        formatter_class = argparse.RawDescriptionHelpFormatter,  # don't wrap my description
        fromfile_prefix_chars = '@'
    )

    parser.add_argument (
        'images', metavar='FILENAME', type=str, nargs='+',
        help='the images to upload'
    )

    parser.add_argument (
        '-v', '--verbose', dest='verbose', action='count',
        help='increase output verbosity', default=0
    )
    parser.add_argument (
        '-n', '--dry-run', dest='dry_run', action='store_true',
        help='dry run: do not upload any images',
    )
    parser.add_argument (
        '-t', '--t_max', type = float, metavar='SECONDS',
        help='max time delta between images in sequence', default=DEFAULT_MAX_TIME
    )
    parser.add_argument (
        '-d', '--d_max', type = float, metavar='METERS',
        help='max distance between images in sequence', default=DEFAULT_MAX_DIST
    )
    parser.add_argument (
        '--dop_max', type = float, metavar='DOP',
        help='discard images with GPS DOP greater than this', default=DEFAULT_MAX_DOP
    )
    return parser


def build_list (args):
    ''' Build a list of files to upload '''

    geotags = []
    discarded = 0
    errors = 0

    for filename in args.images:
        try:
            gt = read_sidecar_file (filename)
        except (OSError, json.decoder.JSONDecodeError) as e:
            errors += 1
            sys.stderr.write (str (e))
            continue

        if gt.get ('status_code', 0) == 204:
            discarded += 1
            if args.verbose:
                sys.stderr.write ("Image %s was already uploaded\n" % filename)
            continue

        if 'MAPLatitude' not in gt or 'MAPCaptureTime' not in gt:
            discarded += 1
            if args.verbose:
                sys.stderr.write ("No GPS data for file %s\n" % filename)
            continue

        if gt.get ('MAPDOP', 1.0) > args.dop_max:
            discarded += 1
            if args.verbose:
                sys.stderr.write ("Max GPS DOP exceeded in file %s\n" % filename)
            continue

        geotags.append (gt)

    if args.verbose:
        print ("%d images were discarded and %d had errors"
               % (discarded, errors))

    return geotags


def upload_image_file (args, session, geotags):
    ''' Upload one image. '''

    try:
        upload_image (session, geotags, args.dry_run)
    except (requests.exceptions.HTTPError, ValueError) as e:
        sys.stderr.write ("Error uploading image: %s\n" % geotags['filename'])
        sys.stderr.write (str (e) + '\n')
    args.pbar.update ()



def upload_sequence (args, sequence):
    ''' Upload a sequence of images. '''

    upload_token = args.config[args.config.sections()[0]]['user_upload_token']
    with managed_session (upload_token, args.dry_run) as session:
        with Pool (UPLOAD_THREADS) as pool:
            pool.starmap (upload_image_file, zip (
                itertools.repeat (args),
                itertools.repeat (session),
                sequence,
            ))


def main ():
    ''' Main function. '''

    args = build_parser ().parse_args ()

    args.config = read_config_file ()

    geotags = build_list (args)
    if len (geotags) == 0:
        if args.verbose:
            print ("No images to upload.")
        return

    geotags = cut_sequences (geotags, args.t_max, args.d_max)
    sequences = [list (v) for k, v in itertools.groupby (
        geotags, operator.itemgetter ('sequence_id'))]

    if args.verbose:
        print ("Sequenced %d images in %d sequences" % (len (geotags), len (sequences)))

    with tqdm (total = len (geotags), desc = 'Dry run' if args.dry_run else 'Uploading',
               unit = 'image', disable = args.verbose == 0) as args.pbar:

        with Pool (SEQUENCE_THREADS) as seq_pool:
            seq_pool.starmap (upload_sequence, zip (
                itertools.repeat (args),
                sequences,
            ))

    if args.verbose:
        print ("Done.")


if __name__ == '__main__':
    main ()

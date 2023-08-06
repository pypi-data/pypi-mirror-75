''' Global Configuration '''

import configparser
from contextlib import contextmanager
import datetime
import getpass
import io
import json
import operator
import os
import re
import uuid

from geopy.distance import geodesic
import piexif
import requests

CLIENT_ID = os.getenv (
    'MAPILLARY_CLIENT_ID',
    'MkJKbDA0bnZuZlcxeTJHTmFqN3g1dzo1YTM0NjRkM2EyZGU5MzBh'
)

CONFIG_FILEPATH = os.getenv (
    'MAPILLARY_CONFIG_FILEPATH',
    os.path.join (os.path.expanduser ('~'), '.config', 'mapillary', 'configs', CLIENT_ID)
)

API_ENDPOINT = 'https://a.mapillary.com'

USERS_ENDPOINT  = API_ENDPOINT + '/v3/users'
LOGIN_ENDPOINT  = API_ENDPOINT + '/v2/ua/login'
UPLOAD_TOKENS_ENDPOINT = API_ENDPOINT + '/v3/users/{user_key}/upload_tokens'
UPLOAD_ENDPOINT = API_ENDPOINT + '/v3/me/uploads'


def get_auth_tokens (user_name, user_email, user_password):
    ''' Get the authorization tokens from the Mapillary API. '''

    try:
        # get user key
        message = 'Error getting user key: No user by name %s.' % user_name
        params = { 'client_id' : CLIENT_ID, 'usernames' : user_name }
        r = requests.get (USERS_ENDPOINT, params = params)
        r.raise_for_status ()
        user_key = r.json ()[0]['key']

        # get upload token
        message = 'Error getting upload token: Wrong email %s or wrong password.' % user_email
        params = { 'client_id' : CLIENT_ID }
        data = { 'email' : user_email, 'password' : user_password }
        r = requests.post (LOGIN_ENDPOINT, params = params, data = data)
        r.raise_for_status ()
        upload_token = r.json ()['token']

        # get user hashes
        message = 'Error getting user hashes.'
        params  = { 'client_id' : CLIENT_ID }
        headers = { 'Authorization' : 'Bearer %s' % upload_token }
        r = requests.get (UPLOAD_TOKENS_ENDPOINT.format (user_key = user_key),
                          params = params, headers = headers)
        r.raise_for_status ()
        j = r.json ()

        return {
            'MAPSettingsUsername'  : user_name,
            'MAPSettingsUserKey'   : user_key,
            'user_upload_token'    : upload_token,
            'user_signature_hash'  : j.get ('images_hash', ''),
            'user_permission_hash' : j.get ('images_policy', ''),
            'aws_access_key_id'    : j.get ('aws_access_key_id', ''),
        }

    except (IndexError, KeyError, requests.exceptions.HTTPError):
        print (message)
        raise


def gps_ascii (value):
    ''' Decode ascii bytes to string. '''
    return value.decode ('ascii')

def gps_rational (values):
    ''' Decode exif rational value to float. '''
    return float (values[0]) / float (values [1])


def gps_coordinate (values, reference):
    ''' Decode exif GPS coordinate as float.

    GPS Coordinates are stored as 3 rationals.
    '''

    sign = 1 if gps_ascii (reference) in 'NE' else -1
    degrees, minutes, seconds = map (gps_rational, values)
    return sign * (degrees + minutes / 60 + seconds / 3600)


def get_image_geotags (filename):
    ''' Extract relevant exif tags from image. '''

    # Exif Version 2.3 http://www.cipa.jp/std/documents/e/DC-008-2012_E.pdf

    geotags = {}
    exif_data = piexif.load (filename)
    t = dict (exif_data['0th'])
    t.update (exif_data['Exif'])
    t.update (exif_data['GPS'])

    # lat, long
    try:
        geotags['MAPLatitude']  = gps_coordinate (t[piexif.GPSIFD.GPSLatitude],
                                                  t[piexif.GPSIFD.GPSLatitudeRef])
        geotags['MAPLongitude'] = gps_coordinate (t[piexif.GPSIFD.GPSLongitude],
                                                  t[piexif.GPSIFD.GPSLongitudeRef])
    except KeyError:
        pass

    # altitude
    try:
        sign = -1 if t.get (piexif.GPSIFD.GPSAltitudeRef, 0) else 1
        geotags['MAPAltitude'] = sign * gps_rational (t[piexif.GPSIFD.GPSAltitude])
    except KeyError:
        pass

    # DOP
    try:
        geotags['MAPDOP'] = gps_rational (t[piexif.GPSIFD.GPSDOP])
    except KeyError:
        pass

    # datetime
    subseconds = 0.0
    for f in [piexif.ExifIFD.SubSecTime,
              piexif.ExifIFD.SubSecTimeOriginal,
              piexif.ExifIFD.SubSecTimeDigitized]:
        if f in t:
            subseconds = float (b"0." + t[f])
            break

    for f in [piexif.ImageIFD.DateTime,
              piexif.ExifIFD.DateTimeOriginal,
              piexif.ExifIFD.DateTimeDigitized]:
        if f in t:
            dt = " ".join (re.sub ('[^0-9]', ' ', str (t[f])).split ())
            dt = datetime.datetime.strptime (dt, '%Y %m %d %H %M %S')
            dt += datetime.timedelta (seconds = subseconds)
            geotags['MAPCaptureTime'] = dt.strftime ("%Y_%m_%d_%H_%M_%S_%f")
            break

    # heading
    try:
        heading = gps_rational (t[piexif.GPSIFD.GPSImgDirection]) % 360.0
        ref = 'True' if gps_ascii (t[piexif.GPSIFD.GPSImgDirectionRef]) == 'T' else 'Magnetic'
        geotags["MAPCompassHeading"] = {
            ref + 'Heading' : heading,
        }
    except KeyError:
        pass

    return geotags


def cut_sequences (geotags, time_max, dist_max):
    ''' Build image sequences '''

    geotags = sorted (geotags, key = operator.itemgetter ('MAPCaptureTime'))
    sequence_id = 0
    geotags[0]['sequence_id'] = sequence_id

    for a, b in zip (geotags, geotags[1:]):
        dta = datetime.datetime.strptime (a['MAPCaptureTime'], '%Y_%m_%d_%H_%M_%S_%f')
        dtb = datetime.datetime.strptime (b['MAPCaptureTime'], '%Y_%m_%d_%H_%M_%S_%f')
        timedelta = dtb - dta
        dist = geodesic (
            (a['MAPLatitude'], a['MAPLongitude']),
            (b['MAPLatitude'], b['MAPLongitude'])
        ).m
        if timedelta.total_seconds () > time_max or dist > dist_max:
            # start a new sequence
            sequence_id += 1
        b['sequence_id'] = sequence_id

    return geotags


def get_upload_filename (filename, geotags):
    ''' Generate a filename for the uploaded image. '''

    _, ext = os.path.splitext (filename) # pylint: disable=unused-variable
    try:
        ch = geotags['MAPCompassHeading']['TrueHeading']
    except KeyError:
        ch = 0.0
    return '{MAPLatitude}_{MAPLongitude}_{ch}_{MAPCaptureTime}_{MAPPhotoUUID}{ext}'.format (
        ch = ch, ext = ext, **geotags)


def upload_image (session, geotags, dry_run):
    ''' Upload one image to the server. '''

    filename = geotags['filename']
    upload_filename = get_upload_filename (filename, geotags)

    data = session['fields'].copy ()
    data['key'] = session['key_prefix'] + upload_filename

    with open (filename, 'rb') as fpin:

        # put a json dump of the geotags into the image description field
        exif_dict = piexif.load (fpin.read ())
        filtered_geotags = { k: v for k, v in geotags.items () if k.startswith ('MAP') }
        exif_dict['0th'][piexif.ImageIFD.ImageDescription] = json.dumps (filtered_geotags)

        # insert exif data into memory buffer
        fpout = io.BytesIO ()
        fpin.seek (0)
        try:
            piexif.insert (piexif.dump (exif_dict), fpin.read (), fpout)
        except ValueError as e:
            raise Exception ("Error: invalid Exif data in image: %s\n" % filename) from e

        # and upload the memory buffer
        if dry_run:
            geotags['status_code'] = 204
        else:
            r = requests.post (session['url'], data = data,
                               files = { 'file' : (upload_filename, fpout) })
            geotags['status_code']  = r.status_code
            geotags['uploaded_timestamp'] = datetime.datetime.utcnow ().isoformat ()
            geotags['uploaded_filename']  = upload_filename
            geotags['uploaded_sequence_key'] = session['key']
            del geotags['sequence_id']
            write_sidecar_file (filename, geotags)
            r.raise_for_status ()

    return True


def create_session (upload_token):
    ''' Create a new upload session. '''

    params  = { "client_id" : CLIENT_ID }
    headers = { "Authorization" : "Bearer " + upload_token }
    payload = { "type" : "images/sequence" }

    r = requests.post (UPLOAD_ENDPOINT, params = params, headers = headers, json = payload)
    r.raise_for_status()
    return r.json ()


def close_session (session, upload_token):
    ''' Close an upload session. '''

    url = '{endpoint}/{key}/closed'.format (endpoint = UPLOAD_ENDPOINT, key = session['key'])
    params  = { "client_id" : CLIENT_ID }
    headers = { "Authorization" : "Bearer " + upload_token }

    r = requests.put (url, params = params, headers = headers)
    r.raise_for_status()


@contextmanager
def managed_session (upload_token, dry_run):
    ''' A context manager for sessions. '''

    if dry_run:
        session =  {
            'fields'     : {},
            'key_prefix' : '',
        }
    else:
        session = create_session (upload_token)

    try:
        yield session

    finally:
        if not dry_run:
            close_session (session, upload_token)


def read_config_file (filename = CONFIG_FILEPATH):
    ''' Read the configuration file. '''

    config = configparser.ConfigParser ()
    config.optionxform = str # make option names case sensitive
    config.read (filename)
    return config


def write_config_file (tokens, filename = CONFIG_FILEPATH):
    ''' Write the configuration file. '''

    config = read_config_file (filename)

    section = tokens['MAPSettingsUsername']
    config[section] = tokens

    # file contains sensitive information so make it chmod 600
    with open (os.open (filename, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600), 'w') as fp:
        config.write (fp)


def get_sidecar_filename (image_filename):
    ''' return the sidecar filename for the image. '''

    return image_filename + '.mapillary'


def read_sidecar_file (image_filename):
    ''' Read the sidecar file for image. '''

    try:
        sidecar = get_sidecar_filename (image_filename)
        with open (sidecar, 'r') as fp:
            data = json.loads (fp.read ())
            data['filename'] = image_filename
            return data
    except OSError as e:
        return { 'filename' : image_filename }
    except json.decoder.JSONDecodeError:
        raise Exception ("JSON syntax error in sidecar file %s\n" % sidecar) from e


def write_sidecar_file (image_filename, geotags):
    ''' Write the sidecar file for image. '''

    with open (get_sidecar_filename (image_filename), 'w') as fp:
        fp.write (json.dumps (geotags, sort_keys = True, indent = 4))

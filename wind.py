#!/usr/bin/env python

"""Download and process the latest wind data

Usage:
  get-latest.py [--date=<YYYYMMDD>]
  get-latest.py [--dest=<filepath>]
  get-latest.py (-h | --help)
  get-latest.py --version

Options:
  -h --help          Show this screen.
  --version          Show version.
  --date=<YYYYMMDD>  Process wind data from a specific date.
  --dest=<filepath>  Destination filepath for the resulting JSON file

"""
from docopt import docopt
import datetime
from subprocess import call
import os
import errno
import urllib2
from time import strftime


def download_data(date):
    """Download wind data from NOAA.

    Downloads the GRIB (GRIdded Binary or General Regularly-distributed
    Information in Binary form) wind data from NOAA.
    Saves it in the data directory, adding a date string to the filename.

    Args:
        date: A string indicating the date of the data we want.

    Returns:
        A string of the downloaded GRIB filename.

    """

    iso_date_frag = (datetime.datetime.strptime(date, '%Y%m%d')
                     .strftime('%Y-%m-%d'))

    url = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs.pl' + '?' + \
        'file=gfs.t00z.pgrbf00.grib2&' + \
        'lev_10_m_above_ground=on&' + \
        'var_UGRD=on&var_VGRD=on&' + \
        'dir=%2Fgfs.' + date + '00'
    print url

    file_name = iso_date_frag + '_gfs.t00z.pgrbf00.grib2'
    try:
        u = urllib2.urlopen("%s" % (url))
        f = open('data/' + file_name, 'wb')
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            f.write(buffer)
        f.close()
        return f.name
    except urllib2.HTTPError, e:
        print('HTTPError = ' + str(e.code))
    except urllib2.URLError, e:
        print('URLError = ' + str(e.reason))


def grib_2_json(grib_file, datestring,
                dest=None,
                apppath='/Applications/grib2json-0.8.0-SNAPSHOT/bin'):
    """Convert GRIB file to JSON.

    Converts the GRIB wind data into a JSON file that the Earth visualization
    system can read. Saves the file in date directories where Earth can
    access them. This assumes that you've setup Earth in your
    ~/src/wind/ directory.

    Args:
        grib_file: A string representing the filename of the GRIB file
        to be converted.
        datestring: A string representing the YYYYMMDD that this
        GRIB file represents
        dest: A string. The destination path for the JSON file.
        apppath: A string. The path to the grib2json script.

    Returns:
        A string of the converted JSON filename.

    """
    # Base dir for the weather data
    if dest is None:
        dest = (os.path.expanduser("~") +
                os.sep + 'src/wind/public/data/weather')

    current = (dest + os.sep + 'current' + os.sep +
               'current-wind-surface-level-gfs-1.0.json')

    # Data is read from year, month, and day directories,
    # so we need to create them.
    d = datetime.datetime.strptime(datestring, '%Y%m%d')
    dest = (os.path.normpath(dest) + os.sep +
            d.strftime('%Y') + os.sep +
            d.strftime('%m') + os.sep +
            d.strftime('%d') + os.sep)
    create_path(dest)

    # Convert files with the grib2json utility
    cmd = os.path.normpath(apppath) + os.sep + 'grib2json'
    dest = dest + '0000-wind-surface-level-gfs-1.0.json'
    cmd = (cmd + ' -d -n -o ' + dest + ' ' + grib_file)
    call(cmd, shell=True)

    # Make a symlink to the new file from the "current" path
    os.remove(current)
    os.symlink(dest, current)

    return dest


def create_path(path):
    """Try to create all the directories for a given filepath

    Args:
        path: A string of the filepath to create
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Get Latest Data 0.0.1')
    if arguments['--date'] is None:
        date = datetime.datetime.now().strftime('%Y%m%d')
    else:
        date = arguments['--date']
    grib_file = download_data(date)
    json_file = grib_2_json(grib_file, date, arguments['--dest'])

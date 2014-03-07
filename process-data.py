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

    url = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs.pl' + '?' + \
        'file=gfs.t00z.pgrbf00.grib2&' + \
        'lev_10_m_above_ground=on&' + \
        'var_UGRD=on&var_VGRD=on&' + \
        'dir=%2Fgfs.' + strftime('%Y%m%d') + '00'

    # Prefix the filename with an ISO date fragment
    iso_date_frag = (datetime.datetime.strptime(date, '%Y%m%d')
                     .strftime('%Y-%m-%d'))
    file_name = iso_date_frag + '_gfs.t00z.pgrbf00.grib2'

    # Open URL, download it, and write it to a file
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


def grib_2_json(grib_file, datestring,
                dest=None,
                path='/Applications/grib2json-0.8.0-SNAPSHOT/bin'):
    # Base dir for the weather data
    if dest is None:
        dest = (os.path.expanduser("~") +
                os.sep + 'src/wind/public/data/weather')

    # Data is read from year, month, and day directories,
    # so we need to create them.
    d = datetime.datetime.strptime(datestring, '%Y%m%d')
    dest = (os.path.normpath(dest) + os.sep +
            d.strftime('%Y') + os.sep +
            d.strftime('%m') + os.sep +
            d.strftime('%d') + os.sep)
    print dest
    create_path(dest)

    # Convert files with the grib2json utility
    cmd = os.path.normpath(path) + os.sep + 'grib2json'
    cmd = (cmd + ' -d -n -o ' +
           dest + '0000-wind-surface-level-gfs-1.0.json ' + grib_file)
    print cmd
    call(cmd, shell=True)


def create_path(path):
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

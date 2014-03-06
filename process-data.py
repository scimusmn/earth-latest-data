#!/usr/bin/env python

"""Download and process the latest wind data

Usage:
  get-latest.py [--date=<YYYYMMDD>]
  get-latest.py (-h | --help)
  get-latest.py --version

Options:
  -h --help          Show this screen.
  --version          Show version.
  --date=<YYYYMMDD>  Process wind data from a specific date.

"""
from docopt import docopt

import datetime
import urllib2
from time import strftime


def download_data(date):

    if date is None:
        date = datetime.datetime.now().strftime('%Y%m%d')

    url = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs.pl' + '?' + \
        'file=gfs.t00z.pgrbf00.grib2&' + \
        'lev_10_m_above_ground=on&' + \
        'var_UGRD=on&var_VGRD=on&' + \
        'dir=%2Fgfs.' + strftime('%Y%m%d') + '00'

    # Prefix the filename with an ISO date fragment
    iso_date_frag = (datetime.datetime.strptime(date, '%Y%m%d')
                     .strftime('%Y-%m-%d'))
    file_name = iso_date_frag + '_gfs.t00z.pgrbf00.grib2'

    u = urllib2.urlopen("%s" % (url))
    f = open('data/' + file_name, 'wb')

    # Unused - NEED?
    #meta = u.info()
    # Progress meter - NOT WORKING
    #file_size = int(meta.getheaders("Content-Length")[0])
    #print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        # Progress meter - NOT WORKING
        #status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        #status = status + chr(8)*(len(status)+1)
        #print status,

    f.close()

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Get Latest Data 0.0.1')
    download_data(arguments['--date'])

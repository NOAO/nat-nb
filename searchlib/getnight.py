#! /usr/bin/env python
"""GIVEN: caldat, prop_id
RETURN: files ingested on CALDAT that are associated with Proposal prop_id
"""
# Python library
import sys
import argparse
import datetime
import shutil
from pathlib import Path
# External Packages
import requests
from astropy.utils.data import download_file

def get_files(propid, caldat, download_dir='~/Downloads'):
    """Download files matching query from Archive."""
    # propid = '2020A-0399'
    # caldat = '2020-02-10'
    outdir = str(Path(download_dir).expanduser())
    today = str(datetime.datetime.now().date())
    adsurl='https://astroarchive.noao.edu/api/adv_search/fasearch/?limit=9'
    jj = {
        "outfields" : ['archive_filename'],
        "search" : [
            ["release_date", '1900-01-01', today],
            ["caldat", caldat, caldat],
            ["proposal", propid]
        ]
    }
    
    
    for idx,row in enumerate(requests.post(adsurl,json=jj).json()):
        try:
            fname = download_file(row['url'],
                                cache=False, show_progress=True, timeout=120)
            outfile = Path(outdir,Path(row['archive_filename']).name)
            shutil.move(fname, outfile)
        except Exception as err:
            print(f'Could not download using {row["url"]}; {str(err)}')
    return idx



##############################################################################

def main():
    """Parse command line arguments and do the work."""
    parser = argparse.ArgumentParser(
        description='Get a nights worth of FITS file for one Proposal',
        epilog='EXAMPLE: ./%(prog)s 2020A-0399 2020-02-10'
        )
    default_dir = '~/Downloads'
    parser.add_argument('propid', 
                        help='Proposal ID (e.g. 2020A-0399)')
    parser.add_argument('caldat', 
                        help='Night of file collection (e.g. 2020-02-10)')
    parser.add_argument('-d', '--downloaddir',
                        default=default_dir,
                        help=('Directory to put downloaded FITS files into. '
                              f'[default="{default_dir}"]'
                              ))
    args = parser.parse_args()

    cnt = get_files(args.propid, args.caldat,
                    download_dir=args.downloaddir)
    print(f'Stored {cnt} files into {args.downloaddir}')

if __name__ == '__main__':
    main()

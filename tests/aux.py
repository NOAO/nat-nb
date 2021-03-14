#! /usr/bin/env python
'''\
Report info from scraping notebooks.  UNDER CONSTRUCTION
'''
## Standard Python library
import sys, argparse, logging
## External packages
import nbformat
## Local packages
# <none>


nb_list = [
    'utils.ipynb',
    'sia.ipynb',
    'advanced-search.ipynb',
    'api-authentication.ipynb',
    'exposure-map.ipynb',
    ]

def get_runtimes(notebooks=nb_list):
    rt = dict()
    for nbfilename in notebooks:
        nb = nbformat.read(nbfilename,nbformat.NO_CONVERT)
        code_cells = [c for c in nb.cells if c.cell_type == 'code']
        #!outstrs = [out.text for out in code_cells[-1].outputs if out.get('name') == 'stdout']
        #!if len(outstrs) > 0:
        #!    outstr = outstrs[0]
        #!    # e.g. 'Elapsed seconds=16.806087795994245 on https://astroarchive.noirlab.edu\n'
        #!
        #!    outstr.split()[1].split('=')[1]
        #!    secs = float(outstr.split()[1].split('=')[1])

        results = [out.get('data').get('text/plain') for out in code_cells[-1].outputs if out.output_type=='execute_result']
        if len(results) > 0:
            secs = float(results[0])
        else:
            secs = -60
        rt[nbfilename] = secs
    return rt
        

def gen_report():
    runtimes = get_runtimes()
    print ('Notebook runtimes (minutes):')
    print('\n'.join([f'  {float(v/60.0):6.1f}: {k}' for k,v in runtimes.items()]))


##############################################################################

def my_parser():
    parser = argparse.ArgumentParser(
        #!version='1.0.1',
        description='My shiny new python program',
        epilog='EXAMPLE: %(prog)s a b"'
        )
    #!parser.add_argument('--outfile', help='File in which to write report',
    #!                    type=argparse.FileType('w') )

    parser.add_argument('--loglevel',      help='Kind of diagnostic output',
                        choices = ['CRTICAL','ERROR','WARNING','INFO','DEBUG'],
                        default='WARNING',
                        )
    return parser

def main():
    parser = my_parser()
    args = parser.parse_args()
    #!args.outfile.close()
    #!args.outfile = args.outfile.name

    #!print 'My args=',args
    #!print 'infile=',args.infile


    log_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(log_level, int):
        parser.error('Invalid log level: %s' % args.loglevel) 
    logging.basicConfig(level = log_level,
                        format='%(levelname)s %(message)s',
                        datefmt='%m-%d %H:%M'
                        )
    logging.debug('Debug output is enabled!!!')

    gen_report()

if __name__ == '__main__':
    main()

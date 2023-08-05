#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
This module is an OpenTrep binding.

 >>> from OpenTrepWrapper import main_trep, index_trep
 >>> from OpenTrepWrapper import DEFAULT_LOG, DEFAULT_FMT, DEFAULT_IDX, DEFAULT_POR
 
 >>> index_trep (porPath = '/tmp/opentraveldata/optd_por_public_all.csv', \
                 xapianDBPath = '/tmp/opentrep/xapian_traveldb', \
                 logFilePath = '/tmp/opentrep/opeentrep-indexer.log', \
                 verbose = False)

 >>> main_trep (searchString = 'nce sfo', \
                outputFormat = 'S', \
                xapianDBPath = '/tmp/opentrep/xapian_traveldb', \
                logFilePath = '/tmp/opentrep/opeentrep-searcher.log', \
                verbose = False)
 ([(89.8466, 'NCE'), (357.45599999999996, 'SFO')], '')

'''

from __future__ import with_statement

import json
import sys
import os, errno

try:
    # For 64 bits system, if not in site-packages
    sys.path.append ('/usr/lib64')

    # Initialise the OpenTrep C++ library
    import pyopentrep

except ImportError:
    # pyopentrep could not be found
    raise ImportError("*pyopentrep* raised ImportError.")


# Default settings
DEFAULT_POR = '/tmp/opentraveldata/optd_por_public.csv'
DEFAULT_IDX = '/tmp/opentrep/xapian_traveldb'
DEFAULT_FMT = 'S'
DEFAULT_LOG = '/tmp/opentrep/opentrepwrapper.log'
FLAG_INDEX_NON_IATA_POR = False
FLAG_INIT_XAPIAN = True
FLAG_ADD_POR_TO_DB = True

AVAILABLE_FORMATS = set(['I', 'J', 'F', 'S'])



class OpenTrepLib(object):
    '''
    This class wraps the methods of the C++ OpenTrepSearcher class.

    >>> otp = OpenTrepLib(DEFAULT_POR, DEFAULT_IDX, DEFAULT_LOG)

    >>> otp.search('san francsico los angeles', DEFAULT_FMT)
    ([(0.32496, 'SFO'), (0.5450269999999999, 'LAX')], '')

    >>> otp.finalize()
    '''

    def __init__(self, porPath=DEFAULT_POR, xapianDBPath=DEFAULT_IDX, logFilePath=DEFAULT_LOG):

        if not os.path.isdir(xapianDBPath):
            # If xapianDBPath is not a directory,
            # it probably means that the database has
            # never been created
            # First we create the path to avoid failure next
            print('/!\ Directory {} did not exist, creating...\n'.format(xapianDBPath))
            mkdir_p(xapianDBPath)

        self._trep_lib = pyopentrep.OpenTrepSearcher ()

        # sqlDBType = 'sqlite'
        # sqlDBConnStr = '/tmp/opentrep/sqlite_travel.db'
        sqlDBType = 'nodb'
        sqlDBConnStr = ''
        deploymentNumber = 0
        xapianDBActualPath = xapianDBPath + str(deploymentNumber)
        initOK = self._trep_lib.init (porPath, xapianDBPath,
                sqlDBType, sqlDBConnStr,
                deploymentNumber, FLAG_INDEX_NON_IATA_POR,
                FLAG_INIT_XAPIAN, FLAG_ADD_POR_TO_DB, logFilePath)

        if not initOK:
            msgStr = 'Xapian index: {}; SQL DB type: {}; Deployment: {}; log file: {}'.format (xapianDBPath, sqlDBType, deploymentNumber, logFilePath)
            raise Exception('The OpenTrep library cannot be initialised - {}'.format(msgStr))

        if not os.listdir(xapianDBActualPath):
            # Here it seems that the xapianDBPath is empty,
            # this is the case if the POR data file has not been indexed yeet.
            # So we index the POR data file now with Xapian.
            print('/!\ {} seems to be empty, forcing indexation now...\n'.format(xapianDBPath))
            self.index(verbose=True)


    def finalize(self):
        '''
        Free the OpenTREP library resource
        '''
        self._trep_lib.finalize()


    def __enter__(self):
        '''To be used in with statements.
        '''
        return self


    def __exit__(self, type_, value, traceback):
        '''On de-indent inside with statement.
        '''
        self.finalize()


    def getPaths(self):
        '''
        File-paths details
        '''
        # Calls the underlying OpenTrep library service
        filePathList = self._trep_lib.getPaths().split(';')

        # Report the results
        print("ORI-maintained list of POR (points of reference): '%s'" % filePathList[0])
        print("Xapian-based travel database/index: '%s'" % filePathList[1])


    def index(self, verbose=False):
        '''
        Indexation
        '''
        if verbose:
            print("Perform the indexation of the (Xapian-based) travel database.")
            print("That operation may take several minutes on some slow machines.")
            print("It takes less than 20 seconds on fast ones...")

        # Calls the underlying OpenTrep library service
        result = self._trep_lib.index()

        if verbose:
            # Report the results
            print("Done. Indexed %s POR (points of reference)" % result)



    def search(self, searchString, outputFormat=DEFAULT_FMT, verbose=False):
        '''Search.

        If no search string was supplied as arguments of the command-line,
        ask the user for some

        Call the OpenTrep C++ library.

        The 'I' (Interpretation from JSON) output format is just an example
        of how to use the output generated by the OpenTrep library. Hence,
        that latter does not support that "output format". So, the raw JSON
        format is required, and the JSON string will then be parsed and
        interpreted by the jsonResultParser() method, just to show how it
        works
        '''

        if outputFormat not in AVAILABLE_FORMATS:
            raise ValueError('outputFormat "%s" invalid, not in %s.' % \
                             (outputFormat, AVAILABLE_FORMATS))

        opentrepOutputFormat = outputFormat

        if opentrepOutputFormat == 'I':
            opentrepOutputFormat = 'J'

        result = self._trep_lib.search(opentrepOutputFormat, searchString)

        # When the compact format is selected, the result string has to be
        # parsed accordingly.
        if outputFormat == 'S':
            fmt_result = compactResultParser(result)

        # When the full details have been requested, the result string is
        # potentially big and complex, and is not aimed to be
        # parsed. So, the result string is just displayed/dumped as is.
        elif outputFormat == 'F':
            fmt_result = result

        # When the raw JSON format has been requested, no handling is necessary.
        elif outputFormat == 'J':
            fmt_result = result

        # The interpreted JSON format is an example of how to extract relevant
        # information from the corresponding Python structure. That code can be
        # copied/pasted by clients to the OpenTREP library.
        elif outputFormat == 'I':
            fmt_result = jsonResultParser(result)

        if verbose:
            print(' -> Raw result: %s' % result)
            print(' -> Fmt result: %s' % str(fmt_result))

        return fmt_result



def compactResultParser(resultString):
    '''
    Compact result parser. The result string contains the main matches,
    separated by commas (','), along with their associated weights, given
    as percentage numbers. For every main match:

     - Columns (':') separate potential extra matches (i.e., matches with the same
       matching percentage).
     - Dashes ('-') separate potential alternate matches (i.e., matches with lower
       matching percentages).

    Samples of result string to be parsed:

     % python3 pyopentrep.py -f S nice sna francisco vancouver niznayou
     'nce/100,sfo/100-emb/98-jcc/97,yvr/100-cxh/83-xea/83-ydt/83;niznayou'
     % python3 pyopentrep.py -f S fr
     'aur:avf:bae:bou:chr:cmf:cqf:csf:cvf:dij/100'

    >>> test_1 = 'nce/100,sfo/100-emb/98-jcc/97,yvr/100-cxh/83-xea/83-ydt/83;niznayou'
    >>> compactResultParser(test_1)
    ([(1.0, 'NCE'), (1.0, 'SFO'), (1.0, 'YVR')], 'niznayou')

    >>> test_2 = 'aur:avf:bae:bou:chr:cmf:cqf:csf:cvf:dij/100'
    >>> compactResultParser(test_2)
    ([(1.0, 'AUR')], '')

    >>> test_3 = ';eeee'
    >>> compactResultParser(test_3)
    ([], 'eeee')
    '''

    # Strip out the unrecognised keywords
    if ';' in resultString:
        str_matches, unrecognized = resultString.split(';', 1)
    else:
        str_matches, unrecognized = resultString, ''

    if not str_matches:
        return [], unrecognized


    codes = []

    for alter_loc in str_matches.split(','):

        for extra_loc in alter_loc.split('-'):

            extra_loc, score = extra_loc.split('/', 1)

            for code in extra_loc.split(':'):

                codes.append((float(score) / 100.0, code.upper()))

                # We break because we only want to first
                break

            # We break because we only want to first
            break

    return codes, unrecognized



def jsonResultParser(resultString):
    '''
    JSON interpreter. The JSON structure contains a list with the main matches,
    along with their associated fields (weights, coordinates, etc).
    For every main match:

     - There is a potential list of extra matches (i.e., matches with the same
       matching percentage).
     - There is a potential list of alternate matches (i.e., matches with lower
       matching percentages).

    Samples of result string to be parsed:

     - python3 pyopentrep.py -f J nice sna francisco
       - {'locations':[
            {'names':[
               {'name': 'nice'}, {'name': 'nice/fr:cote d azur'}],
             'city_code': 'nce'},
            {'names':[
               {'name': 'san francisco'}, {'name': 'san francisco/ca/us:intl'}],
             'city_code': 'sfo',
             'alternates':[
                  {'names':[
                      {'name': 'san francisco emb'},
                      {'name': 'san francisco/ca/us:embarkader'}],
                      'city_code': 'sfo'},
                  {'names':[
                      {'name': 'san francisco jcc'},
                      {'name': 'san francisco/ca/us:china hpt'}],
                      'city_code': 'sfo'}
            ]}
         ]}

     - python3 pyopentrep.py -f J fr
       - {'locations':[
            {'names':[
               {'name': 'aurillac'}, {'name': 'aurillac/fr'}],
                'extras':[
                {'names':[
                  {'name': 'avoriaz'}, {'name': 'avoriaz/fr'}],
                'city_code': 'avf'},
               {'names':[
                  {'name': 'barcelonnette'}, {'name': 'barcelonnette/fr'}],
                'city_code': 'bae'}
            ]}
         ]}

    >>> res = """{ "locations":[{
    ...                 "iata_code": "ORY",
    ...                 "icao_code": "LFPO",
    ...                 "city_code": "PAR",
    ...                 "geonames_id": "2988500",
    ...                 "lon": "2.359444",
    ...                 "lat": "48.725278",
    ...                 "page_rank": "23.53"
    ...             }, {
    ...                 "iata_code": "CDG",
    ...                 "icao_code": "LFPG",
    ...                 "city_code": "PAR",
    ...                 "geonames_id": "6269554",
    ...                 "lon": "2.55",
    ...                 "lat": "49.012779",
    ...                 "page_rank": "64.70"
    ...             }]
    ... }"""
    >>> print(jsonResultParser(res))
    ORY-LFPO-2988500-23.53%-PAR-48.73-2.36; CDG-LFPG-6269554-64.70%-PAR-49.01-2.55
    '''

    return '; '.join(
        '-'.join([
            loc['iata_code'],
            loc['icao_code'],
            loc['geonames_id'],
            '%.2f%%' % float(loc['page_rank']),
            loc['cities']['city_details']['iata_code'],
            '%.2f' % float(loc['lat']),
            '%.2f' % float(loc['lon'])
        ])
        for loc in json.loads(resultString)['locations']
    )



def mkdir_p(path):
    '''
    mkdir -p behavior.
    '''
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def index_trep (porPath = DEFAULT_POR,
                xapianDBPath = DEFAULT_IDX,
                logFilePath = DEFAULT_LOG,
                verbose=False):
    '''
    Instanciate the OpenTrepLib object and index.
    '''
    with OpenTrepLib(porPath, xapianDBPath, logFilePath) as otp:
        otp.index(verbose)


def main_trep (searchString,
               outputFormat = DEFAULT_FMT,
               xapianDBPath = DEFAULT_IDX,
               logFilePath = DEFAULT_LOG,
               verbose = False):
    '''
    Instanciate the OpenTrepLib object and search from it.

    >>> main_trep (searchString = 'san francisco', \
                   outputFormat = 'S', \
                   xapianDBPath = '/tmp/opentrep/xapian_traveldb', \
                   logFilePath = '/tmp/opentrep/opeentrep-searcher.log', \
                   verbose = False)
    ([(0.32496, 'SFO')], '')

    '''
    with OpenTrepLib(DEFAULT_POR, xapianDBPath, logFilePath) as otp:
        return otp.search(searchString, outputFormat, verbose)


def _test():
    '''
    Launching doctests.
    '''
    import doctest

    opt = doctest.ELLIPSIS

    doctest.testmod(optionflags=opt)


if __name__ == '__main__':

    _test()


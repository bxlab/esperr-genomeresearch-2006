#!/usr/bin/env python2.3

"""
Chops alignments in a MAF file to piece of a specified length. A random set of
non overlapping chunks of exactly the specified chop length will be produced
"""

import sys

import ranges, sys, random
from align import maf
from optparse import OptionParser

def __main__():

    # Parse command line arguments

    parser = OptionParser()
    parser.add_option( "-l", "--length", action="store", type="int", default=100, help="" )

    ( options, args ) = parser.parse_args()

    length = options.length
    maf_reader = maf.Reader( sys.stdin )
    maf_writer = maf.Writer( sys.stdout )

    for m in maf_reader:

        maf_length = m.text_size
        chunk_count = maf_length // length
        lost_bases = maf_length % length
        skip_amounts = [0] * ( chunk_count + 1 )
        for i in range( 0, lost_bases ): skip_amounts[ random.randrange( 0, chunk_count + 1 ) ] += 1

        start = 0
        for i in range( 0, chunk_count ):
            start += skip_amounts[ i ]
            n = m.slice( start, start + length )
            if check_len( n ): maf_writer.write( m.slice( start, start + length ) )
            start += length

def check_len( a ):
    for c in a.components:
        if c.size == 0: return False
    return True 
    

if __name__ == "__main__": __main__()

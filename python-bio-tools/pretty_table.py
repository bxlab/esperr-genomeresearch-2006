#!/usr/bin/env python

import sys

def main():
    pad = "\t"
    if len( sys.argv ) > 1:
        pad = " " * int( sys.argv[1] )
    rows = [ line.split() for line in sys.stdin ]
    print_tabular( rows, pad )

def print_tabular( rows, pad, align=None ):
    if len( rows ) == 0: return ""
    lengths = [ len( col ) for col in rows[ 0 ] ]
    for row in rows[1:]:
        for i in range( 0, len( row ) ):
            lengths[ i ] = max( lengths[ i ], len( row[ i ] ) )
    rval = ""
    for i in range( len( rows[0] ) ):
        if align and align[ i ] == "l":
            rval += str( i ).ljust( lengths[ i ] )
        else:
            rval += str( i ).rjust( lengths[ i ] )
        rval += pad 
    print rval   
    for row in rows:
        rval = ""
        for i in range( 0, len( row ) ):
            if align and align[ i ] == "l":
                rval += row[ i ].ljust( lengths[ i ] )
            else:
                rval += row[ i ].rjust( lengths[ i ] )
            rval += pad
        print rval

main()

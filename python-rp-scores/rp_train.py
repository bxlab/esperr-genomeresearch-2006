#!/usr/bin/env python2.3

"""
Train a discriminating model from two data sets and store it.

usage: %prog pos_data neg_data out [options]
   -f, --format=FILE:  Format of input data. 'ints' by default, or 'maf'
   -m, --mapping=FILE: A mapping (alphabet reduction) to apply to each sequence (optional)
   -r, --radix=N:      Radix
   -o, --order=N:      Order
"""

import align.maf
import array
import cookbook.doc_optparse
import sys
import traceback

import rp.io
import rp.mapping
import rp.standard_model

def run( pos_file, neg_file, out_file, format, mapping, radix, order ):

    # Read integer sequences
    pos_strings = list( rp.io.get_reader( pos_file, format, mapping ) )
    neg_strings = list( rp.io.get_reader( neg_file, format, mapping ) )

    # Determine radix
    if not radix:
        if mapping: radix = mapping.get_out_size()
        else: radix = max( map( max, pos_strings ) + map( max, neg_strings ) ) + 1
        
    # Build model
    model = rp.standard_model.train( order, radix, pos_strings, neg_strings )

    # Write to out file
    model.to_file( out_file )

def main():

    # Parse command line
    try:
        options, args = cookbook.doc_optparse.parse( __doc__ )
        pos_fname, neg_fname, out_fname = args
        order = int( getattr( options, 'order' ) )
        radix = getattr( options, 'radix', None )
        format = getattr( options, 'format', None )
        if options.mapping:
            mapping = rp.mapping.alignment_mapping_from_file( file( options.mapping ) )
        else:
            mapping = None
    except:
        cookbook.doc_optparse.exit()

    out = open( out_fname, "w" )
    run( open( pos_fname ), open( neg_fname ), out, format, mapping, radix, order )
    out.close()

if __name__ == "__main__": main()

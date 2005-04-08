#!/usr/bin/env python2.3

"""
Score a set of alignments (MAF format) using a model

usage: %prog data score_matrix out [options]
   -m, --mapping=FILE: A mapping (alphabet reduction) to apply to each sequence (optional)
   -M, --model=MODEL:  Name of model to use
   -w, --window=N:     Size of window to scroll over sequence (default 100)
   -s, --shift=N:      Amount to shift window (deafult 5)
   -b, --low=N:        Truncate to this minimum score
   -e, --high=N:       Truncate to this maximum score
"""

try: 
    import psyco
    psyco.full()
except: 
    pass

import align.maf
import array
import cookbook.doc_optparse
import seq_numarray
import sys
import traceback

import rp.io 
import rp.mapping
import rp.models

def run( data_file, modname, model_file, out_file, mapping, window, shift, low, high ):

    # Read model
    model = rp.models.get( modname ).from_file( model_file )
    radix = model.get_radix()

    # Open maf file
    mafs = align.maf.Reader( data_file )

    # Score each alignment
    for maf in mafs:
        ints = rp.mapping.DNA.translate_list( [ c.text for c in maf.components ] )
        if mapping: ints = mapping.translate( ints )
        score_windows( maf, array.array( 'i', list( ints ) ), model, out_file, window, shift, low, high )

def score_windows( maf, string, model, out, window, shift, low, high ):
    if maf.text_size < window: return
    half_window = window // 2
    rc = maf.components[0] 
    text = rc.text
    # Output position is middle of window
    abs_pos = rc.start + ( half_window - text.count( '-', 0, half_window ) ) 
    last_pos = None
    chrom = rc.src
    if '.' in chrom: chrom = chrom.split('.')[1]
    #print >>out, "variableStep chrom=" + chrom
    print >>out, "fixedStep chrom=%s start=%d step=%d" % ( chrom, abs_pos, shift )
    for i, c in enumerate( text ):
        if i + window >= len( text ): break
        if c != '-': abs_pos += 1
        if abs_pos % shift == 0:
            score = model.score( string, i, window )
            if score is not None:
                if abs_pos == last_pos: continue
                if score > high: score = high
                elif score < low: score = low
                # print >>out, abs_pos, round( score, 6 )
                print >>out, round( score, 6 )
                last_pos = abs_pos

def getopt( options, name, default ):
    v = getattr( options, name )
    if v is None: return default
    return v

def main():

    # Parse command line
    options, args = cookbook.doc_optparse.parse( __doc__ )
    #try:
    if 1:
        data_fname, model_fname, out_fname = args
        window = int( getopt( options, 'window', 100 ) )
        shift = int( getopt( options, 'shift', 5 ) )
        low = float( getopt( options, 'low', -1.0 ) )
        high = float( getopt( options, 'high', 1.0 ) )
        if options.mapping:
            align_count, mapping = rp.mapping.alignment_mapping_from_file( file( options.mapping ) )
        else:
            mapping = None
        modname = getattr( options, 'model' )
        if modname is None: modname = 'standard'
    #except:
    #    cookbook.doc_optparse.exit()

    out = open( out_fname, "w" )
    run( open( data_fname ), modname, open( model_fname ), out, mapping, window, shift, low, high )
    out.close()

if __name__ == "__main__": main()

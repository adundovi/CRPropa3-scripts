#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

def count_lines( filename ):
    """ Count lines in a file given by filename """
    return sum( 1 for line in open( filename ) if '#' not in line )

def guess_order( filename ):
    """ Return the order of columns based on a comment in the first line of the file """
    with open( filename, 'r') as f:
        header = f.readline()
    
    if not header.startswith('#'):
        sys.exit( "Missing header in input_file" )
    
    column_names = header[1:].split()

    return column_names

def read_array( filename ):
    """ Read out the content of a file and return it in a list of lists """
    array = []

    with open( filename, 'r') as f:
         for line in f:
             if line.startswith('#'):
                 continue
             array.append( line.split() )

    return array

def main():
    if len(sys.argv) < 3:
        sys.exit( "script_name input_file output_file ['arbitrary column order']" )

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    target_order = "D, ID, ID0, E, E0, X, Y, Z, X0, Y0, Z0, Px, Py, Pz, P0x, P0y, P0z, z".split(", ")
    if len(sys.argv) == 4:
        target_order = sys.argv[3].split()


    input_data = read_array( input_file )
    output_data = [ [ "0" for col in xrange( len( target_order ) ) ] for row in xrange( count_lines( input_file ) ) ]

    input_order = guess_order( input_file )

    print "From: ", input_order
    print "To: ", target_order

    for new_col in enumerate( target_order ):
        if new_col[1] in input_order:
            pos = input_order.index(new_col[1])
        else:
            continue
        for i in xrange( len( output_data ) ):
            output_data[i][new_col[0]] = input_data[i][pos]

    with open( output_file, 'w') as f:
        f.write( '#\t' + '\t'.join( target_order ) + '\n' )
        for line in output_data:
            f.write( '\t'.join( line ) + '\n' )

if __name__ == "__main__":
    main()

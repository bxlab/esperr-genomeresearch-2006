def get( name ):
    try:
        return getattr( __import__( "rp.models", globals(), locals(), [ name ] ), name )
    except:
        raise "Unknown model: '%s'" % name
        
def train( modname, *args ):
    
    if ":" in modname:
        name, modargs = modname.split( ':' )
        kwargs = dict( [ arg.split( '=' ) for arg in modargs.split( ',' ) ] )
    else:
        name = modname
        kwargs = dict()
    
    return get( name ).train( *args, **kwargs )
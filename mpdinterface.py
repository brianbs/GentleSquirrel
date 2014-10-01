"""
The MPD Interface
"""
from mpd import MPDClient

class MPDInterface( MPDClient ):
    """
    Just extended the MPDClient class to have __enter__ and __exit__ methods,
    so I can use it properly with a "with' statement
    """
    def __init__( self, host="localhost", port=6600 ):
        super( MPDInterface, self ).__init__()
        self.timeout = 10
        self.connect( host, port )

    def add( self, filename ):
        super( MPDInterface, self ).add( filename )
        if self.status()['state'] == "stop":
            self.play()

    def __enter__( self ):
        return self

    def __exit__( self, type, value, traceback ):
        self.close()
        self.disconnect()

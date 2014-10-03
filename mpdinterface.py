"""
The MPD Interface
"""
from mpd import MPDClient
from time import sleep

class MPDInterface( MPDClient ):
    """
    Just extended the MPDClient class to have __enter__ and __exit__ methods,
    so I can use it properly with a "with' statement
    """
    def __init__( self, host="localhost", port=6600 ):
        super( MPDInterface, self ).__init__()
        self.timeout = 10
        self.connect( host, port )


    def add( self, filename, new_file = False ):
        """
        """
        if new_file:
            self.update()
        new_file_added = False
        for i in range( 10 ):
            try:
                super( MPDInterface, self ).add( filename )
                new_file_added = True
            except Exception as e:
                # If this is a new file, the database might still be updating
                # so we sleep for 3 seconds and try again.  If it's not new,
                # just throw the exception
                if new_file:
                    sleep( 3 )
                    continue
                else:
                    raise e
            else:
                break
        if new_file and not new_file_added:
            raise Exception( "New audo file could not be added" )
        if self.status()['state'] == "stop":
            self.play()

    def __enter__( self ):
        return self

    def __exit__( self, type, value, traceback ):
        self.close()
        self.disconnect()

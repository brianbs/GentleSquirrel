from threading import Thread
from Queue import Queue
from settings import MUSIC_DIR, MPD_HOST, MPD_PORT
from mpdinterface import MPDInterface
from time import sleep

class DLQueue( Queue ):
    def __init__( self ):
        Queue.__init__( self )
        self.dl_threads = []
        for i in range(10):
            t = Thread( target = DLQueue.download_thread, args = (self, ) )
            t.daemon = True
            t.start()
            self.dl_threads.append( t )

    def put( self, source ):
        if not source.is_valid():
            raise Exception( "Not a valid source" )
        Queue.put( self, source )
    
    @staticmethod
    def download_thread( queue ):
        while True:
            source = queue.get()
            file_name = source.download( MUSIC_DIR )
            with MPDInterface( MPD_HOST, MPD_PORT ) as mpd:
                mpd.update()
                for i in range(10):
                    try:
                        mpd.add( file_name )
                    except:
                        sleep( 3 )
                        continue
                    else:
                        break

"""
resources.py

This file contains all of the REST resources
"""
from flask_restful import Resource, reqparse
from util import get_youtube_details
from mpdinterface import MPDInterface
from settings import MPD_HOST, MPD_PORT, MUSIC_DIR
from flask import jsonify, request
from sources import youtube
from jobqueue import JobQueue
from time import sleep

# Instantiate our job queue for downloads
jobq = JobQueue()

# Set the consumer function for the job queue.  Now anything put in the job
# queue will be processed by this function
@jobq.consumer
def download_source( source ):
    metadata = source.download( MUSIC_DIR )
    if metadata is not None:
        music_dir = MUSIC_DIR + "/" if MUSIC_DIR[-1] != "/" else MUSIC_DIR
        filename = metadata.filepath.split( music_dir )[-1]
        with MPDInterface( MPD_HOST, MPD_PORT ) as mpd:
            mpd.add( filename, new_file = True )
    else:
        raise Exception( "Download method returned no metadata" )

def create_error( message, status_code ):
    """
    Short-hand method for returning an API error
    """
    response = jsonify( {'message': message} )
    response.status_code = status_code
    return response

class QueueAPI( Resource ):
    """
    This resource represents the current MPD playlist.  This is the resource
    used to add music to the queue.
    """
    def __init__( self ):
        self.postreqparse = reqparse.RequestParser()
        self.postreqparse.add_argument( 'source-type', type = str,
                default = "youtube", location = "json" )
        self.postreqparse.add_argument( 'source', type = str, required = True,
                help = "No source specified to add!", location = "json" )
        super( QueueAPI, self ).__init__()

    def get( self ):
        """
        Returns a list of songs in the current playlist, along with their length
        """
        with MPDInterface( MPD_HOST, MPD_PORT ) as mpd:
            files = [ {'file': f['file'], 'len': f['time'] } for f in mpd.playlistinfo()]
        return jsonify( {'playlist':files} )
    
    def put( self ):
        """
        Put a representation of a playlist to replace the current playlist
        """
        args = request.get_json()
        with MPDInterface( MPD_HOST, MPD_PORT ) as mpd:
            mpd.clear()
            for f in args['playlist']:
                if 'file' in f:
                    try:
                        mpd.add( f['file'] )
                    except:
                        continue
            files = [ {'file': f['file'], 'len': f['time']} for f in mpd.playlistinfo() ]
        return jsonify( {'playlist':files} )

    def post( self ):
        """
        This is the method used to add music to the current playlist
        """
        print request.get_json()
        args = self.postreqparse.parse_args()
        if args[ 'source-type' ] == "youtube":
            yt = youtube.YTInterface( args[ 'source' ] )
            # First, just try to add the song.  If it can't be added, then it
            # must not be cached:
            if yt.is_valid():
                try:
                    with MPDInterface( MPD_HOST, MPD_PORT ) as mpd:
                        mpd.add( yt.filename )
                    return jsonify( {'message': 
                        '%s retrieved from cache and added to queue.' %\
                                yt.vid_details['title']} )
                except:
                    jobq.add( yt )
            else:
                return create_error( "Could not find the requested song.", 404 )
            return jsonify( {'message': '"%s" [%ss] added to download queue.' %\
                    (yt.vid_details['title'], yt.vid_details['length'])} )
        else:
            return create_error( "Unknown source-type!  Could not queue.", 400 )

class CurrentSongAPI( Resource ):
    def __init__( self ):
        self.postreqparse = reqparse.RequestParser()
        self.postreqparse.add_argument( "operation", required = True,
                help = "No currentsong operation specified", location = "json" )
        super( CurrentSongAPI, self ).__init__()
    
    def get( self ):
        with MPDInterface( MPD_HOST, MPD_PORT ) as mpd:
            curr = mpd.currentsong()
        return jsonify( curr )

    def post( self ):
        args = self.postreqparse.parse_args()
        if args['operation'] == "next":
            with MPDInterface( MPD_HOST, MPD_PORT ) as mpd:
                mpd.next()
                current_song = mpd.currentsong()
        else:
            return create_error( "Invalid operation specified", 400 )
        return jsonify( current_song )

class PlaybackAPI( Resource ):
    """
    This API is used to control the playback state (stop, play pause) of the MPD
    server
    """
    def __init__( self ):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument( 'playback', type = str, required = True,
                help = "No playback state specified", location = "json" )
        super( PlaybackAPI, self ).__init__()

    def get( self ):
        """
        Gets the playback state
        """
        with MPDInterface( MPD_HOST, MPD_PORT ) as mpd:
            state = mpd.status()['state']
        return jsonify( {'playback' : state} )

    def put( self ):
        """
        Changes the playback state
        """
        args = self.reqparse.parse_args()
        with MPDInterface( MPD_HOST, MPD_PORT ) as mpd:
            if args['playback'] == "play":
                mpd.play()
            elif args['playback'] == "pause":
                mpd.pause(1)
            elif args['playback'] == "stop":
                mpd.stop()
            else:
                return create_error( "Invalid playback state specified", 400 )
            state = mpd.status()['state']
        return jsonify( {'playback': state } )

class VolumeAPI( Resource ):
    """
    This resource is used to control the volume
    """
    def __init__( self ):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument( 'volume', type = int, required = True,
                help = "No volume specified!", location = "json" )
        super( VolumeAPI, self ).__init__()

    def get( self ):
        """
        Get the volume
        """
        with MPDInterface( MPD_HOST, MPD_PORT ) as mpd:
            volume = mpd.status()['volume']
        return jsonify( { "volume" : volume } )

    def put( self ):
        """
        Set the volume
        """
        args = self.reqparse.parse_args()
        if args[ 'volume' ] < 0 or args['volume'] > 100:
            return create_error( "Volume specified is out of range", 400 )
        with MPDInterface( MPD_HOST, MPD_PORT ) as mpd:
            mpd.setvol( args['volume'] )
        return jsonify({ 'volume': args['volume'] })

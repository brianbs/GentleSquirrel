"""
This file contains all of the logic for interfacing with the youtube API and
downloading music
"""
from gdata.youtube.service import YouTubeService, YouTubeVideoQuery
from source import SourceBase
from settings import MUSIC_DIR
from subprocess import Popen, PIPE

class YTInterface( SourceBase ):
    """
    The interface to the you tubes
    """
    def __init__( self, search ):
        """
        """
        self.search = search
        self.vid_details = self._get_youtube_details()
        # This output format is 
        self.filename = self.vid_details['title'] + "-" + self.vid_details['id'] + ".aac"
        # This replace is neccessary because youtube dl replaces double quotes with single quotes
        self.filename = self.filename.replace( '"', "'" )

    def is_valid( self ):
        """
        """
        if self.vid_details is None:
            return False
        return True

    def download( self, out_dir ):
        """
        """
        vid_details = self.vid_details
        if vid_details is None:
            return False
        p = Popen( ["youtube-dl", "-x", "--audio-format", "aac", "-o",
            out_dir + "/%(title)s-%(id)s.%(ext)s", vid_details['url']],
            stdout = PIPE )
        stdout = p.communicate()[0]
        if p.returncode != 0:
            return None
        vid_output = ""
        for line in stdout.split("\n"):
            if "Destination" in line and ".aac" in line:
                vid_output = line.split( "Destination:" )[1].strip().\
                        split(MUSIC_DIR)[-1][1:]
        return None if vid_output == "" else vid_output

    def _get_youtube_details( self ):
        """
        This method queries the youtube API for details on the specified video
        """
        yt_service = YouTubeService()
        query = YouTubeVideoQuery()
        query.vq = self.search
        query.racy = 'include'
        query.orderby = 'relevance'
        feed = yt_service.YouTubeQuery( query )
        if len( feed.entry ) > 0:
            return { 'id': feed.entry[0].id.text.split('/')[-1],
                    'url': feed.entry[0].GetSwfUrl(),
                    'title': feed.entry[0].media.title.text,
                    'length': feed.entry[0].media.duration.seconds }
        else:
            return None

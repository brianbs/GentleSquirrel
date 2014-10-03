from abc import ABCMeta, abstractmethod
from collections import namedtuple

# Metadata object.  This is how the calling thread will know where the
# downloaded file ended up
Metadata = namedtuple( 'Metadata', ['filename', 'filepath', 'title', 'len'] )

class SourceBase( object ):
    """
    This class is a base class for all the different source types (youtube,
    reddit, soundcloud, etc).  Might be overkill, but meh
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def download( self, out_dir ):
        """
        Subclasses should implement this as a method that downloads an audio
        file to the specified output directory, and should return a metadata
        tuple if successful, or None if unsuccessful
        """
        return

    @abstractmethod
    def is_valid( self ):
        """
        This method must return true for a download to be added to the download
        queue
        """
        return

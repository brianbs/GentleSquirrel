from abc import ABCMeta, abstractmethod

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
        file to the specified output directory, and should return the location 
        of the downloaded file if successful, or none if unsuccessful
        """
        return

    @abstractmethod
    def is_valid( self ):
        """
        This method must return true for a download to be added to the download
        queue
        """
        return

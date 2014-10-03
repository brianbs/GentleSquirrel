from threading import Thread
from Queue import Queue

class JobQueue():
    """
    An extremely minimal job queue / threadpool
    """
    def __init__( self, num_processes = 10, default_consumer = None ):
        """
        Creates a queue to hold the jobs, launches the worker threads, and,
        optionally, registers a default consumer
        """
        self._q = Queue()
        self._worker_threads = []
        self._default_consumer = default_consumer
        for i in range( num_processes ):
            t = Thread( target = JobQueue.__work_func, args = (self._q, ) )
            t.daemon = True
            t.start()
            self._worker_threads.append( t )

    def add( self, job_description, worker = None ):
        """
        Add a job to the queue, and specify the consumer function to perform
        that job.  If no consumer function is specified, the default consumer
        is used
        """
        worker = self._default_consumer if worker is None else worker
        self._q.put( (job_description, worker) )

    @staticmethod
    def __work_func( queue ):
        """
        In this function, each thread pops a job off the queue and performs it
        """
        while True:
            job_description, callback = queue.get()
            try:
                callback( job_description )
            except:
                continue

    def register_consumer( self, consumer ):
        """
        Register a default consumer function
        """
        self._default_consumer = consumer

    def consumer( self, func ):
        """
        Does the same thing as register_consumer, but can be used as a decorator
        to specify the consumer function
        """
        self._default_consumer = func
        return func

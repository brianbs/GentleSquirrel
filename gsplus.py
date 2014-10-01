from flask import Flask
from flask_restful import Api
from resources import QueueAPI, PlaybackAPI, VolumeAPI
from multiprocessing import Pool

# Initialize the app and the flask_restful API
app = Flask( __name__ )
api = Api( app )

# Register the different resources / endpoints with the API
api.add_resource( QueueAPI, "/gsplus/api/v0.1/queue" )
api.add_resource( PlaybackAPI, "/gsplus/api/v0.1/state/playback" )
api.add_resource( VolumeAPI, "/gsplus/api/v0.1/state/volume" )

if __name__ == "__main__":
    app.run( debug = True )

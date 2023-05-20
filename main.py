import spot
from setup import *

logger = create_logger(__name__)
cli_args = get_cli_args()

play = spot.SpotifyPlaylist(cli_args=cli_args)
play.create_spotify_client()
play.get_artist_ids()
play.get_track_recommendations()
play.create_playlist()
play.add_tracks_to_playlist()

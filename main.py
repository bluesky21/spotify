import spot
from setup import *

logger = create_logger(__name__)
cli_args = get_cli_args()

if cli_args.artists:
    # build using artist seeds
    play = spot.ArtistSeedPlaylist(cli_args=cli_args)
else:
    play = spot.SavedTracksSeedPlaylist(cli_args=cli_args)

play.get_track_recommendations()
play.create_playlist()
play.add_tracks_to_playlist()

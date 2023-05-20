from yaml import safe_load
from typing import Dict, Any, List
from dataclasses import dataclass
import spotipy
from setup import create_logger

@dataclass
class SpotifyPlaylist:
    """
    Create playlist based off recommendation results from list of seed artists

    Params
    ------
    `config_path`
        Path to local config file
    `cli_args`
        CLI Arguments: seed artists, playlist name, public/private
    """
    cli_args:Dict[str, Any]
    config_path:str = 'config.yaml'
    

    def __post_init__(self):
        self.logger = create_logger(__name__)
        self._get_config()
        self.CONSTANTS = self.CONFIG['constants']
        self._get_api_creds()
        self._parse_cli_args()


    def _parse_cli_args(self):
        """Dynamically assign attributes from CLI Args"""
        for name, val in vars(self.cli_args).items():
            setattr(self, name, val)


    def _get_config(self):
        """Get local config file"""
        with open(self.config_path, 'r') as f:
            self.CONFIG = safe_load(f)
        

    def _get_api_creds(self):
        """Get Spotify App creds"""
        with open(self.CONFIG['creds']['path'], 'r') as f:
            self.API_CREDS = safe_load(f)
        

    def _oauth(self):
        """
        Use Spotipy to go through OAuth2 process. 
        Needed to be able to get User info
        """
        self.sp_oauth = spotipy.oauth2.SpotifyOAuth(
            client_id = self.API_CREDS['client_id'],
            client_secret = self.API_CREDS['client_secret'],
            redirect_uri = self.CONSTANTS['redirect_uri'],
            scope = self.CONSTANTS['scopes']
        )


    def create_spotify_client(self):
        """Instantiate instance of Spotify client"""
        self._oauth()
        self.spotify_client = spotipy.Spotify(auth_manager=self.sp_oauth)
        self._get_user_id()


    def _get_user_id(self):
        """Get Spotify User Id. Used to know where to create playlist"""
        self.user_id = self.spotify_client.me()['id']


    @staticmethod
    def _get_artist_id(client, artist:str):
        """Get the Artist Id for a single artist name"""
        result = client.search(artist)
        return result['tracks']['items'][0]['artists'][0]['id']
    

    def get_artist_ids(self):
        """Create dict of artist and id for `cli_arg.artist` list"""
        if self.artists is not None:
            self.artist_ids = {artist: self._get_artist_id(self.spotify_client, artist) for artist in self.artists}


    def get_track_recommendations(self):
        """Get list of recommendations based on Artist list from CLI"""
        rec = self.spotify_client.recommendations(
                    seed_artists=self.artist_ids.values(),
                    country=self.CONSTANTS['country']
        )
        self.rec_track_ids = [track['id'] for track in rec['tracks']]


    def create_playlist(self):
        """Create a new empty playlist"""
        new_pl = self.spotify_client.user_playlist_create(
                    user=self.user_id,
                    name=self.playlist,
                    public=self.public,
                    description=f'Seeded using recommendations from {", ".join(self.artists)}'
        )
        self.playlist_id:str = new_pl['id']


    def add_tracks_to_playlist(self):
        """Populate newly created playlist with recommendations from seed artists"""
        self.spotify_client.playlist_add_items(
            playlist_id=self.playlist_id,
            items=self.rec_track_ids
        )

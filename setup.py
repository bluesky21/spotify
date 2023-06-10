import argparse
from typing import Dict, Any
import logging
import sys

def get_cli_args() -> Dict[str, Any]:
    # allows for interactive dev
    sys.argv = [""]
    parser = argparse.ArgumentParser(description='CLI Args for creating Spotify playlists using seed artists')
    parser.add_argument(
        '-p', '--playlist',
        help='Name of playlist to be created',
        type=str
    )
    parser.add_argument(
        '-a', '--artists',
        help='Artist names to find recommendations from. Comma separated. Double quotes artists with spaces in name',
        nargs='+',
        type=str,
        required=False
    )
    parser.add_argument(
        '--public',
        help='If flag is passed the playlist is created publicly',
        default=False   
    )
    return parser.parse_args()


def create_logger(module_name):
    logger = logging.getLogger(module_name)
    logging.basicConfig(
        level='WARN',
        datefmt='%Y-%m-%d %H:%M'
        )
    return logger

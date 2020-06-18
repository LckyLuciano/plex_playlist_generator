import argparse
import random
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi.playlist import Playlist
from plexapi.exceptions import NotFound
import tvdb_api
import re
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

PL_TITLE = '- Random Episodes of Good Shows -'
# list of series to include
WHITELIST = ['Another Period',
             'Aqua Teen Hunger Force',
             'Beavis and Butthead',
             'Broad City',
             'Curb Your Enthusiasm',
             'Dual Survival',
             'Flight of the Conchords',
             'Futurama',
             'Getting On (US)',
             'Good Eats',
             'It\'s Always Sunny in Philadelphia',
             'Jeopardy!',
             'Key & Peele',
             'King of the Hill',
             'Letterkenny',
             'Modern Family',
             'Parks and Recreation',
             'Party Down',
             'South Park',
             'The Life & Times of Tim',
             'The Office (US)',
             'The Price Is Right',
             'Veep',
             'Workaholics'
            ]

def get_args():
    parser = argparse.ArgumentParser(description='Create playlist of unwatched episodes from random shows '
                                                 'but in correct episode order.')
    parser.add_argument('--name', help='Playlist Name', default='- Random Episodes of Good Shows -')
    parser.add_argument('--number', '-n', help='Number of episodes to add to play list', type=int, default=300)
    group_server = parser.add_argument_group('Server Connection Method')
    group_server.add_argument('--server', action='store_true', help='Server connection Method')
    group_server.add_argument('--baseurl', '-b', help='Base URL of Server')
    group_server.add_argument('--token', '-t', help='Authentication Token')
    group_account = parser.add_argument_group('Plex Account Connection Method')
    group_account.add_argument('--account', action='store_true', help='Account Connection Method')
    group_account.add_argument('--username', '-u', help='Plex Account Username')
    group_account.add_argument('--password', '-p', help='Plex AccountPassword')
    group_account.add_argument('--resource', '-r', help='Resource Name (Plex Server Name)')
    parser.add_argument('--debug', '-d', help='Debug Logging', action="store_true")
    return parser.parse_args()


def get_random_episodes(all_shows, n=200):
    show_episodes = dict()
    for show in all_shows.all():
        if show.title not in WHITELIST:
            continue
        show_episodes[show.title] = show.episodes()
    next_n = []
    while len(next_n) < n:
        show_name = random.choice(list(show_episodes.keys()))
        print(show_episodes[show_name])
        next_n.append(random.choice(show_episodes[show_name]))
    return next_n


def tvdb_season_count(show, season):
    try:
        tvdb_id = int(re.search('thetvdb://([0-9]+)?', show.guid).group(1))
        tv = tvdb_api.Tvdb(language='en')
        season_list = tv[tvdb_id][season]
        return len(season_list)
    except tvdb_api.tvdb_seasonnotfound:
        return None


def skipped_missing(show, episode):
    try:
        season_num = episode.seasonNumber
        episode_num = episode.index

        if episode.index > 1:
            show.get(season=episode.seasonNumber, episode=episode.index-1)
            return False
        elif episode.seasonNumber > 1:
            previous_season_count = tvdb_season_count(show, season_num - 1)
            if previous_season_count is None:
                return False
            # check last episode of previous season
            show.get(season=episode.seasonNumber - 1, episode=previous_season_count)
            return False
        else:
            return False
    except NotFound:
        return True


def main():
    args = get_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    if args.account:
        # ## Connect via Account
        account = MyPlexAccount(args.username, args.password)
        plex = account.resource(args.resource).connect()
    elif args.server:
        # ## Connect via Direct URL
        baseurl = args.baseurl
        token = args.token
        plex = PlexServer(baseurl, token)
    else:
        exit(1)
    #update tv library name here >>>> 
    all_shows = plex.library.section('HD TV Shows')
    # shows = get_unwatched_shows(all_shows.all())
    episodes = get_random_episodes(all_shows, n=args.number)
    for episode in episodes:
        season_episode = episode.seasonEpisode
        # skipped = skipped_missing(all_shows.get(title=episode.grandparentTitle), episode)

    # playlist = Playlist(plex, )
    plex.playlist(title=args.name).delete()
    Playlist.create(server=plex, title=args.name, items=episodes)


if __name__ == '__main__':
    main()

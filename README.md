# Plex Random Series Playlist Generator

A fork of robobeaver6's fine work, dumbed down for a simpleton like me, working on python3. The main feature i changed is it'll just grab any random episodes from any tv show on a whitelist.

##Usage
```
playlist_generator.py [-h] [--name NAME] [--number NUMBER] [--server]
                             [--baseurl BASEURL] [--token TOKEN] [--account]
                             [--username USERNAME] [--password PASSWORD]
                             [--resource RESOURCE] [--debug]

Create playlist of unwatched episodes from random shows but in correct episode
order.

optional arguments:
  -h, --help                         show this help message and exit
  --name NAME                        Playlist Name
  --number NUMBER, -n NUMBER         Number of episodes to add to play list
  --debug, -d                        Debug Logging

Server Connection Method:
  --server                           Server connection Method
  --baseurl BASEURL, -b BASEURL      Base URL of Server
  --token TOKEN, -t TOKEN            Authentication Token

Plex Account Connection Method:
  --account                          Account Connection Method
  --username USERNAME, -u USERNAME   Plex Account Username
  --password PASSWORD, -p PASSWORD   Plex AccountPassword
  --resource RESOURCE, -r RESOURCE   Resource Name (Plex Server Name) 
```
## Connection Methods
### Account
Uses your PlexTV Account, username and Resource Name (Server Name)  
e.g. `playlist_generator.py --account --username MyUserName --password Sh1tPass --resource MyServer`

### Server
Uses The Server URL and Authentication Token  
e.g. `playlist_generator.py --server --baseurl "http://172.16.1.100:32400" --token "fR5GrDxfLunKynNub5"`

### Authentication Token
To get your Auth token, browse to an episode in the web UI. Click on the `...` video and select `Get Info`.  In the 
popup window select `View XML` in the URL there is the `X-Plex-Token=XXXXXXXXXXXXXX`

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred
import sys

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_ID, client_secret= cred.client_SECRET, redirect_uri=cred.redirect_url ,scope=scope))

def defaultScript():
    results = sp.current_user_saved_tracks()
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], "-", track['name'])
    return

def LikedSongsBackup():
    print("Start of writting \n")
    fileObject = open("likedSongs.txt", "w+")
    offset = 0
    results = sp.current_user_saved_tracks(20,offset)
    fileObject.write("Liked songs back up: \n \n")
    
    while(sp.next(results)):
        results = sp.current_user_saved_tracks(20,offset)
        for idx, item in enumerate(results['items']):
            track = item['track']
            outputString = str(idx + offset) +" "+ track['artists'][0]['name'] + " - " + track['name'] +"\n"
            fileObject.write(outputString)
        offset += 20
        
    print("End of writting ")
    return

def PlayListsBackup():
    offset = 0
    playlists = sp.current_user_playlists()
    for i, playlist in enumerate(playlists['items']):
        fileObject = open("PlaylistBackup" + playlist['name'] +".txt", "w+")
        print(str(offset) + " " + playlist['name'])
        offset += 1
        print("the playlist id: " + playlist['id'])
        fileObject.write(playlist['name'] + "\n \n")
        results = sp.user_playlist_tracks(sp.current_user(),playlist['id'])
        trackList = getPlaylistTracks(sp.current_user(), playlist['id'], fileObject)
        fileObject.close()
    return

def getPlaylistTracks(user, playlist_id, fileObject):
    results = sp.user_playlist_tracks(user, playlist_id)
    tracks = results['items']
    trackNames =[]
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    i = 1
    listlen = len(tracks)
    while i < listlen:
        trackNames.extend(tracks[i]['track']['name'])
        fileObject.write(str(i) + " ")
        fileObject.write(tracks[i]['track']['name'])
        fileObject.write("\n")
        #print(tracks[i]['track']['name'])
        i+= 1
    return trackNames

if (sys.argv[1] == "s"):
    LikedSongsBackup()
    
elif (sys.argv[1] == 'p'):
    PlayListsBackup()
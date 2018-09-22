import sys
import spotipy
import spotipy.util as util
import operator

scope = 'user-library-read'

def show_playlist_artists(tracks):
	artist_list = []
	for i, item in enumerate(tracks['items']):
		track = item['track']
		artist_list.append(track['artists'][0]['id'])
	return artist_list


if len(sys.argv) > 1:
	#username = sys.argv[1]
	username = "sceenaroonies"
else:
	print("Usage: %s username" % (sys.argv[0],))
	sys.exit()

token = util.prompt_for_user_token(username, scope)

if token:
	sp = spotipy.Spotify(auth=token)
	playlists = sp.user_playlists(username)
	for playlist in playlists['items']:
		if playlist['name'] == "Thursdaze":
			print("")
			print(playlist['name'])
			results = sp.user_playlist(username, playlist['id'],
				fields="tracks")
			tracks = results['tracks']
			playlist_artists = show_playlist_artists(tracks)
			genres = []
			print(playlist_artists)
			for artist_id in playlist_artists:
				if artist_id is not None:
					genres.append(sp.artist(artist_id)['genres'])
			genres = [y for x in genres for y in x]
			dict_genres = dict()
			for genre in genres:
				dict_genres[genre] = dict_genres.get(genre, 0) + 1
			for sortedValue in sorted(dict_genres.values()):
				print(sortedValue)


		
else:
	print("Can't get token for", username)
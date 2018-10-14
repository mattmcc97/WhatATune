import sys
import spotipy
import spotipy.util as util
import operator
import numpy as np
import matplotlib.pyplot as plt
import random
import time

scope = 'user-library-read'

def show_playlist_artists(tracks):
	artist_list = []
	for i, item in enumerate(tracks['items']):
		track = item['track']
		artist_list.append(track['artists'][0]['id'])
	return artist_list

def show_playlist_track_ids(tracks):
	track_ids = []
	for i, item in enumerate(tracks['items']):
		track = item['track']
		track_ids.append(track['id'])
	return track_ids

# t0 = time.time()

if len(sys.argv) > 1:
	username = sys.argv[1]
else:
	print("Usage: %s username" % (sys.argv[0],))
	sys.exit()

token = util.prompt_for_user_token(username, scope, client_id='PLACEHOLDER', client_secret='PLACEHOLDER', redirect_uri='127.0.0.1/callback')

if token:
	sp = spotipy.Spotify(auth=token)
	playlists = sp.user_playlists(username)
	for playlist in playlists['items']:
		#print(playlist['name'])
		if playlist['name'] == "Techno Bunker": #Placeholder Playlist
			# print()
			# print(playlist['name'])
			# print()
			results = sp.user_playlist(username, playlist['id'],
				fields="tracks")
			tracks = results['tracks']
			
			playlist_artists = show_playlist_artists(tracks) #The artist ID of evry song in the playlist
			
			playlist_track_ids = show_playlist_track_ids(tracks) #The track ID of evry song in the playlist

			playlist_audio_features = sp.audio_features(tracks=playlist_track_ids) #The audio analysis for each track in the playlist


			#Numpy arrays containing the tempos, danceability etc. of the songs in a playlist
			tempos = np.empty([1, len(playlist_audio_features)])	
			danceabilities = np.empty([1, len(playlist_audio_features)])
			speechinesses = np.empty([1, len(playlist_audio_features)])
			energies = np.empty([1, len(playlist_audio_features)]) 		

			#Fill in the data in the numpy arrays
			for i, track_feature in enumerate(playlist_audio_features):
				if track_feature is not None: 
					tempos[:, i] = track_feature['tempo']
					danceabilities[:, i] = track_feature['danceability']
					speechinesses[:, i] = track_feature['speechiness']
					energies[:, i] = track_feature['energy']

			#Get the average of each attribute
			avg_tempo = np.mean(tempos)
			avg_danceability = np.mean(danceabilities)
			avg_speechiness = np.mean(speechinesses)
			avg_energy = np.mean(energies)

			#Get the genres of each artist in the playlist, this results in a dictionary
			#containing every genre and hoe many times that genre is in the playlist
			genres = []
			for artist_id in playlist_artists:
				if artist_id is not None:
					genres.append(sp.artist(artist_id)['genres'])
			genres = [y for x in genres for y in x] #Flattens the list of lists
			dict_genres = dict()
			for genre in genres:
				dict_genres[genre] = dict_genres.get(genre, 0) + 1

			#Get the top 5 most common genres in the playlist
			top_5_genres = sorted(dict_genres, key=dict_genres.get, reverse=True)[:5]
			top_5_genres = [genre.replace(" ", "-") for genre in top_5_genres]

			#print(sp.recommendation_genre_seeds())

			#print(top_5_genres)

			#Feed data into the recommendation engine.
			recommendations = sp.recommendations(
				seed_genres=top_5_genres, 
				target_tempo = avg_tempo, min_tempo = avg_tempo - 4, max_tempo = avg_tempo + 4, 
				target_danceability=avg_danceability, min_danceability=avg_danceability - 0.07, max_danceability=avg_danceability + 0.07,
				target_speechiness=avg_speechiness, min_speechiness=avg_speechiness - 0.1, max_speechiness=avg_speechiness+0.1,
				target_energy=avg_energy, min_energy=avg_energy - 0.07, max_energy=avg_energy+0.07
				)

			size_of_recom = len(recommendations['tracks'])

			if(size_of_recom > 0):

				random_song_num = random.randint(0, size_of_recom)

				#Print out the recommended songs to the user, based on the playlist they chose.
				for i in range(0,size_of_recom):
					recommended_song = recommendations['tracks'][i]['name']
					recommended_song_artist = recommendations['tracks'][i]['artists'][0]['name']
					print(recommended_song, "by", recommended_song_artist)

			else:
				print("No recommendations found.")

	# t1 = time.time()
	# print("Total time: ", t1-t0, "(s)")


# {'danceability': 0.763, 
# 'energy': 0.894, 
# 'key': 7, 
# 'loudness': -8.483, 
# 'mode': 1, 
# 'speechiness': 0.0657, 
# 'acousticness': 0.068, 
# 'instrumentalness': 0.931, 
# 'liveness': 0.132, 
# 'valence': 0.341, 
# 'tempo': 126.004, 
# 'type': 'audio_features', 
# 'id': '0dCOxB07cxEtZPfAZmAytj', 
# 'uri': 'spotify:track:0dCOxB07cxEtZPfAZmAytj',
# 'track_href': 'https://api.spotify.com/v1/tracks/0dCOxB07cxEtZPfAZmAytj',
# 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/0dCOxB07cxEtZPfAZmAytj', 
# 'duration_ms': 428095, 
# 'time_signature': 4}

# ,

#  {'danceability': 0.744, 
#  'energy': 0.764, 
#  'key': 6, 
#  'loudness': -9.231,
#  'mode': 0, '
#  'speechiness': 0.0717, 
#  'acousticness': 0.0014,
#  'instrumentalness': 0.857, 
#  'liveness': 0.0674, 
#  'valence': 0.162, 
#  'tempo': 128.024, 
#  'type': 'audio_features',
#  'id': '6bqNhDsfZPOYP3xWDwEzSb', 
#  'uri': 'spotify:track:6bqNhDsfZPOYP3xWDwEzSb',  
#  'track_href': 'https://api.spotify.com/v1/tracks/6bqNhDsfZPOYP3xWDwEzSb',
#  'analysis_url': 'https://api.spotify.com/v1/audio-analysis/6bqNhDsfZPOYP3xWDwEzSb', 
#  'duration_ms': 423750, 
#  'time_signature': 4}


		
else:
	print("Can't get token for", username)
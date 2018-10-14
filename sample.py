import sys
import spotipy
import spotipy.util as util

# scope = 'user-library-read'

# if len(sys.argv) > 1:
#     username = sys.argv[1]
# else:
#     print("Usage: %s username" % (sys.argv[0],))
#     sys.exit()

# token = util.prompt_for_user_token(username, scope)

# if token:
#     sp = spotipy.Spotify(auth=token)
#     results = sp.current_user_saved_tracks()
#     for item in results['items']:
#         track = item['track']
#         print(track['name'] + ' - ' + track['artists'][0]['name'])
# else:
#     print("Can't get token for", username)

# username = 'sceenaroonies' #placeholder value here
# client_id = 'f64ba14936cf46c88401d49b5a94f160' #placeholder value here
# client_secret = '162af3593b654c6b81ddc8b6f9c1c0c5' #placeholder value here
# redirect_uri = '127.0.0.1/callback'

# token = util.prompt_for_user_token(username, client_id, client_secret, redirect_uri)

scope = 'user-library-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

token = util.prompt_for_user_token(username, scope, client_id='f64ba14936cf46c88401d49b5a94f160', client_secret='162af3593b654c6b81ddc8b6f9c1c0c5', redirect_uri='127.0.0.1/callback')

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print(track['name'] + ' - ' + track['artists'][0]['name'])
else:
    print("Can't get token for", username)
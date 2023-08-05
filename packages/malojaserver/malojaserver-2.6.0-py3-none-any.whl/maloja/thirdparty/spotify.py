from . import MetadataInterface, utf, b64
import hashlib
import urllib.parse, urllib.request
import json

class Spotify(MetadataInterface):
	name = "Spotify"

	settings = {
		"apiid":"SPOTIFY_API_ID",
		"secret":"SPOTIFY_API_SECRET"
	}

	metadata = {
		"trackurl": "https://api.spotify.com/v1/search?q={artist}%20{title}&type=track&access_token={token}",
		"artisturl": "https://api.spotify.com/v1/search?q={artist}&type=artist&access_token={token}",
		"response_type":"json",
		"response_parse_tree_track": ["tracks","items",0,"album","images",0,"url"],
		"response_parse_tree_artist": ["artists","items",0,"images",0,"url"],
		"required_settings": ["apiid","secret"],
		"activated_setting": "METADATA_SPOTIFY"
	}

	def authorize(self):

		keys = {
			"url":"https://accounts.spotify.com/api/token",
			"method":"POST",
			"headers":{
				"Authorization":"Basic " + b64(utf(self.settings["apiid"] + ":" + self.settings["secret"])).decode("utf-8")
			},
			"data":bytes(urllib.parse.urlencode({"grant_type":"client_credentials"}),encoding="utf-8")
		}
		req = urllib.request.Request(**keys)
		response = urllib.request.urlopen(req)
		self.settings["token"] = json.loads(response.read())["access_token"]
		return True

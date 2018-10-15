from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = 'AIzaSyBZZ-WR82xzWQKNG_g5lrgciR7ddeu8B4I'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(topic, numVideos):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=topic,
    part='id,snippet',
    maxResults=numVideos,
    type = 'video'
  ).execute()

  videos = []
  channels = []
  playlists = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get('items', []):
    if search_result['id']['kind'] == 'youtube#video':
      videos.append(search_result['id']['videoId'])

    
  return videos


prefix = '<iframe width="560" height="315" src="https://www.youtube.com/embed/'
suffix = '" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>\n'
import json
with open('config.json') as f:
    data = json.load(f)
    
subdir = ['a', 'b']
for sidx, each in enumerate(data['config']):
    urls = []
    videos = youtube_search(each['topic'], each['numVideos'])
    for v in videos:
        urls.append(prefix + v)
    for i in range(each['autoplay']):
        urls[i] = urls[i] + '?&autoplay=1'
    for i in range(each['muted']):
        urls[i] = urls[i] + '&mute=1'
    for i in range(len(urls)):
        urls[i] = urls[i] + suffix
        
    with open("base.html","r") as input:
        contents = input.readlines()

    idx = 0
    while 'iframe' not in contents[idx]:
        idx += 1

    st = idx
    while 'iframe' in contents[idx]:
        idx += 1

    newcontents = contents[:st] + urls + contents[idx:]

    with open(subdir[sidx] + '/index.html',"w") as output:
        output.writelines(newcontents)
